from rest_framework import generics
from ..models import Subject
from .serializers import SubjectSerializer


class SubjectListView(generator.ListAPIView):
    pass
