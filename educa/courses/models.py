from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    """[summary]
    Arguments:
        models {[django]} -- [inheritance]
    Returns:
        [Subject] -- [A subject with a slug and title]
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Course model that defines a complete course that is function
    of a subject.
    Arguments:
        models {Django} -- Django models
    """
    owner = models.ForeignKey(User, related_name='courses_created')
    subject = models.ForeignKey(Subject, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    """[summary]
    Arguments:
        models {[type]} -- [description]
    """
    course = models.ForeignKey(Course, related_name='Modules')
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title
