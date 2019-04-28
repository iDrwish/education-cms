from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .models import Course


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


class OwnerCourseMixin(OwnerMixin):
    model = Course


class OwnerCourseEditMixin(OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView): 
    template_name = 'courses/manage/course/delete.html' 
    success_url = reverse_lazy('manage_course_list')
