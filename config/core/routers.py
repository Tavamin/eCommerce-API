from django.urls import path
from rest_framework_nested import routers
from product.views import CategoryViewSet, ProductViewSet, CommentViewSet
from order.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet, basename='products')
router.register('carts', CartViewSet, basename='carts')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', CommentViewSet, basename='product-comments')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', CartItemViewSet, basename='cart-items')


# URLConf
urlpatterns = router.urls + products_router.urls + cart_items_router.urls
