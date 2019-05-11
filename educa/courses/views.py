from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.forms.models import modelform_factory
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from .models import Course, Module, Content
from .forms import ModuleFormSet


class OwnerMixin(object):
    """
    Defining a mixin to filter the CRUD operations for
    the course by owner.
    Returns:
        querySet -- a filtered queryset with the user
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
    Django mixin to expand the form validation
    to ensure that the form instance user is
    editing a course that he already owns.
    Arguments:
        object {class constrcutor} --
    Returns:
        Form valid -- form valid method
    """
    def form_valid(self, form):
        # validate that form owner is the same as request owner
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(
        PermissionRequiredMixin, OwnerCourseEditMixin,
        CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(
        PermissionRequiredMixin,
        OwnerCourseEditMixin,
        UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    class-based view for routing the dispatcher and building a formset
    for module creation and edit within a Course

    Arguments:
        TemplateResponseMixin {mixin} -- To specify the template_render method
        View {django.views.generic} -- Basic Django generic view

    Returns:
        Formsave in case of a valid formset otherwise error.
    """
    course = None
    template_name = 'courses/manage/module/formset.html'

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """
        Generic get_model method to make sure that the model
        being edited or created is a supported type.
        BONUS: Extend the supported model types by simply adding it in the
        .models and in the below list for validation

        Arguments:
            model_name {str} -- The name of the model being edited or created

        Returns:
            An instance of the model app else None if the name is invalid
        """
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """
        Create a model form from any model

        Arguments:
            model {django.models} -- The model used in the form

        Returns:
            django.form
        """
        Form = modelform_factory(model, exclude=[
            'owner', 'created', 'updated', 'order'],
            )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        Rewrite the dispatch function to do the following:
        1) Verify that the module is owner by the user
        2) Make sure the model name is valid by invoking get_model
        3) Account for ID-based edit
        """
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(
            request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
            )

    def post(self, request, module_id, model_name, id=None):
        """
        Validate the submitted form and coutner for:
        1. New Cotnent being submitted --> id=None
        2. Already exitent content type

        Arguments:
            request
            module_id
            model_name

        Keyword Arguments:
            id -- To extent to edit an already exitent
            Content or a new one. (default: {None})

        Returns:
            form.save() if valid else form
        """
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(
                    module=self.module,
                    item=obj)
            return redirect('module_content_list', self.module_id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
            )


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user
        )
        return self.render_to_response(
            {'module': module}
        )


class ModuleOrderView(
        CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(
        CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})
