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


# ✅ User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ["username", "gender", "modesty_preference", "profile_picture", "bio", "location"]


# ✅ Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


# ✅ SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    # Include category name and ID for context
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)  # Read-only ID

    class Meta:
        model = SubCategory
        fields = ["id", "name", "category_id", "category_name"]


# ✅ Wardrobe Serializer
class WardrobeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    # Keep PrimaryKeyRelatedField for write operations
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True, required=False, allow_null=True
    )
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source="subcategory", write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Wardrobe
        fields = [
            "id", "user", 
            "category", "category_id", 
            "subcategory", "subcategory_id",
            "color", "size", "material", "season", "tags", "photo_path"
        ]
        read_only_fields = ["user", "category", "subcategory"]

    def validate(self, data):
        # Simplified validation - rely on read_only_fields for nested, use IDs for writing
        return data


# ✅ Outfit Serializer
class OutfitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_items = WardrobeSerializer(many=True, read_only=True)
    selected_item_ids = serializers.PrimaryKeyRelatedField(
        queryset=Wardrobe.objects.all(), 
        many=True, 
        write_only=True, 
        source='selected_items'
    )

    class Meta:
        model = Outfit
        fields = ["id", "user", "type", "selected_items", "selected_item_ids", "is_hijab_friendly", "description", "photo_path"]
        read_only_fields = ["user", "selected_items"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Filter items selectable for outfits to the current user's wardrobe
            self.fields['selected_item_ids'].queryset = Wardrobe.objects.filter(user=request.user)


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
