from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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


class Content(models.Model):
    """
    A generic Content model that links to Django ContentType and 
    custom built module type.
    Arguments:
        models {Django} -- Django model builder
    """
    module = models.ForeignKey(Module, related_names='contents')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name="%(class)s_related")
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        asbtract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    text = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Videos(ItemBase):
    url = models.URLField()