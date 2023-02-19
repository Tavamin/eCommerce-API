from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

from .models import Product, Category, Discount, HaveDiscount, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from order.models import OrderItem
from .filters import ProductFilter
from .pagination import DefaultPagination



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'])
        if category.products.count() > 0:
            return Response({'error': 'Cannot delete category with products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'inventory', 'last_update']
    pagination_class = DefaultPagination
    serializer_class = ProductSerializer





    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response({'error': 'Cannot delete product with order items'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'request': self.request, 'product_id': self.kwargs['product_pk']}

