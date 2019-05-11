from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from .models import Course
from .forms import ModuleFormSet


class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super(ManageCourseListView, self()).get_queryset()
        return qs.filter(owner=self.request.user)


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
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerEditMixin):
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
    course = None
    template_name = 'course/manage/module/formset.html'

    def get_formset(self, data=None):
        return ModuleFormSet(self, data=self.data)

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
