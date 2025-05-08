from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, SubCategory, Wardrobe, Outfit, 
    OutfitPlanner, Post, Like, Follow
)

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'gender',
            'modesty_preference',
            'profile_picture',
            'bio',
            'location',
        ]
# ✅ Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        

# ✅ SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'category_id']
        
# ✅ Updated Category Serializer with subcategories
class CategoryWithSubSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']



# ✅ Wardrobe Serializer
class WardrobeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    subcategory = SubCategorySerializer(read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source='subcategory', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Wardrobe
        fields = [
            'id', 'user', 'category', 'category_id', 'subcategory', 'subcategory_id',
            'color', 'size', 'material', 'season', 'tags', 'photo_path'
        ]


# ✅ Outfit Serializer
class OutfitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_items = WardrobeSerializer(read_only=True, many=True)
    selected_items_ids = serializers.PrimaryKeyRelatedField(
        queryset=Wardrobe.objects.all(), many=True, write_only=True, source='selected_items'
    )

    class Meta:
        model = Outfit
        fields = [
            'id', 'user', 'type', 'selected_items', 'selected_items_ids',
            'is_hijab_friendly', 'description', 'photo_path' , 'season', 'tags'
        ]


# ✅ OutfitPlanner Serializer
class OutfitPlannerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    outfit = OutfitSerializer(read_only=True)
    outfit_id = serializers.PrimaryKeyRelatedField(
        queryset=Outfit.objects.all(), source='outfit', write_only=True
    )

    class Meta:
        model = OutfitPlanner
        fields = ['id', 'user', 'outfit', 'outfit_id', 'date']


# ✅ Post Serializer
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    outfit = OutfitSerializer(read_only=True)
    outfit_id = serializers.PrimaryKeyRelatedField(
        queryset=Outfit.objects.all(), source='outfit', write_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'user', 'outfit', 'outfit_id', 'caption', 'created_at']


# ✅ Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post', write_only=True
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'post_id', 'created_at']


# ✅ Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='following', write_only=True
    )

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'following_id', 'created_at']

from .models import Post, Like, Follow

# ✅ Post Serializer
class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at', 'like_count', 'is_liked']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.likes.filter(user=request.user).exists()
        return False

# ✅ Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'

# ✅ Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'
