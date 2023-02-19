"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('core.routers')),
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.jwt')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# def validate(self, attrs):
#     product_id = attrs['product_id']
#     product = ProductSerializer.Meta.model.objects.filter(id=product_id).first()
#     quantity = attrs['quantity']
#     if quantity <= 0:
#         raise serializers.ValidationError('Quantity must be greater than 0')
#     elif quantity > product.inventory:
#         raise serializers.ValidationError('Quantity must be less than inventory')
#     return attrs
#
#
# def create(self, validated_data):
#     cart = self.context['cart']
#     product_id = validated_data['product_id']
#     quantity = validated_data['quantity']
#     cart_item = CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity)
#     return cart_item
#
#
# def update(self, instance, validated_data):
#     instance.quantity = validated_data['quantity']
#     instance.save()
#     return instance
