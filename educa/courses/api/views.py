from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer
from .serializers import CourseWithContentSerializer
from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjetDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @detail_route(
        methods=['get'],
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, requests, *args, **kwargs):
        return self.retrieve(requests, *args, **kwargs)
