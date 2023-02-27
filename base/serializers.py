# external imports
from django.contrib.auth.models import User  # import User model from Django's authentication system
from rest_framework import serializers  # import serializers from Django Rest Framework
from rest_framework_simplejwt.tokens import RefreshToken  # import token generator from JWT

# internal imports
from .models import (
    Product, Review, Order, OrderItem, ShippingAddress
)  # import relevant models from the application


"""
Notes:
    serializers are needed to transform python objects into JSON, and do the reverse process too.
"""

class UserSerializer(serializers.ModelSerializer): # create a serializer for the User model to transform its data for use in the views
    """
    Simple user serielizer class
    """
    # Define fields to include in the serialized output
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    # specify the User model to use in the serializer
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin'] # define which fields to include in the serialized output

    # Define methods to return additional fields for the serialized output
    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer): # create a serializer for the User model to include a JWT token in the serialized output for authentication
    """
    User with JWT token serielizer
    """
    token = serializers.SerializerMethodField(read_only=True)

    # specify the User model to use in the serializer
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    # Define a method to return a JWT token for the serialized output
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ProductSerializer(serializers.ModelSerializer): # create a serializer for the Product model to transform its data for use in the views
    """
    Simple Product Serielizer class
    """
    reviews = serializers.SerializerMethodField(read_only=True)  # Define a field to include related Review objects in the serialized output

    # specify the Product model to use in the serializer
    class Meta:
        model = Product
        fields = (
            'user',
            'name',
            'image',
            'brand',
            'category',
            'description',
            'rating',
            'numReviews',
            'price',
            'countInStock',
            '_id',
            'reviews'
        )  # define which fields to include in the serialized output

    # Define a method to include related Review objects in the serialized output
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer): # create a serializer for the Review model to transform its data for use in the views
    """
    Simple Review Serielizer class
    """

    # specify the Review model to use in the serializer
    class Meta:
        model = Review
        fields = '__all__'  # define which fields to include in the serialized output


class OrderSerializer(serializers.ModelSerializer):
    """
    Simple Review Serielizer class
    """
    orderItems = serializers.SerializerMethodField(read_only=True) # Define a field to include related OrderItem objects in the serialized output
    shippingAddress = serializers.SerializerMethodField(read_only=True)  # Define a field to include related ShippingAddress objects in the serialized output
    user = serializers.SerializerMethodField(read_only=True)  # Define a field to include related User objects in the serialized output


    # specify the Order model to use in the serializer
    class Meta:
        model = Order
        fields = '__all__'  # define which fields to include in the serialized output

    # Define a method to include related OrderItem objects in the serialized output
    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    # Define a method to include related ShippingAddress objects in the serialized output
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    # Define a method to include related User objects in the serialized output
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer): # create a serializer for the OrderItem model to transform its data for use in the views
    """
    Simple OrderItem serielizer class
    """

    # specify the OrderItem model to use in the serializer
    class Meta:
        model = OrderItem
        fields = '__all__'  # define which fields to include in the serialized output


class ShippingAddressSerializer(serializers.ModelSerializer): # create a serializer for the ShippingAddress model to transform its data for use in the views
    """
    simple ShippingAddress serielizer class
    """

    # specify the ShippingAddress model to use in the serializer
    class Meta:
        model = ShippingAddress
        fields = (
            'order',
            'address',
            'city',
            'postalCode',
            'country',
            'shippingPrice',
        )  # define which fields to include in the serialized output