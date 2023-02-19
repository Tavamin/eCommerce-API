from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
# Create your views here.

from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(ModelViewSet):


