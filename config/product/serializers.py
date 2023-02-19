from rest_framework import serializers
from .models import Product, Category, Discount, HaveDiscount, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'image', 'price', 'inventory', 'category',
                  'last_update', 'discounts']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'email', 'name', 'created_at']

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get('user') and not attrs.get('email'):
            raise serializers.ValidationError('User or email is required')
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        if user:
            validated_data['name'] = user.get_full_name()
            validated_data['email'] = user.email
        product_id = self.context['product_id']
        return Comment.objects.create(product_id=product_id, **validated_data)


