from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Wardrobe, Outfit, OutfitPlanner

# ✅ User Serializer (Only basic info)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ✅ UserProfile Serializer (Extra fields like gender, modesty)
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested User data

    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'modesty_preference', 'profile_picture']

# ✅ Wardrobe Serializer
class WardrobeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wardrobe
        fields = '__all__'  # Returns all fields (for flexibility)

# ✅ Outfit Serializer
class OutfitSerializer(serializers.ModelSerializer):
    selected_items = WardrobeSerializer(many=True, read_only=True)

    class Meta:
        model = Outfit
        fields = '__all__'

# ✅ Outfit Planner Serializer
class OutfitPlannerSerializer(serializers.ModelSerializer):
    outfit = OutfitSerializer(read_only=True)

    class Meta:
        model = OutfitPlanner
        fields = '__all__'