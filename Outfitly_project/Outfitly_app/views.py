from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Wardrobe, Outfit, OutfitPlanner
from .serializers import WardrobeSerializer, OutfitSerializer, OutfitPlannerSerializer, UserProfileSerializer
from .models import UserProfile  # Import the UserProfile model
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": username}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# ✅ Register a new user
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)  # ✅ Automatically create UserProfile
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

# ✅ Log in a user
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'message': 'Login successful', 'user_id': user.id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ Get user profile (Requires user ID)
@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

# ✅ Update user profile (gender, modesty_preference, profile picture)
@api_view(['PUT'])
def update_user_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        data = request.data

        profile.gender = data.get('gender', profile.gender)
        profile.modesty_preference = data.get('modesty_preference', profile.modesty_preference)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return Response({'message': 'Profile updated successfully'})
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)



# ✅ Upload Clothing Item (User can add clothes)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_clothing(request):
    """Uploads clothing to the user's wardrobe"""
    serializer = WardrobeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Associate with the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get All Wardrobe Items (User's Clothes)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wardrobe(request):
    """Retrieves all wardrobe items for the logged-in user"""
    items = Wardrobe.objects.filter(user=request.user)
    serializer = WardrobeSerializer(items, many=True)
    return Response(serializer.data)

# ✅ Update Clothing Item
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_clothing(request, item_id):
    """Allows users to edit details of a wardrobe item"""
    try:
        item = Wardrobe.objects.get(id=item_id, user=request.user)
        serializer = WardrobeSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Wardrobe.DoesNotExist:
        return Response({'error': 'Clothing item not found'}, status=status.HTTP_404_NOT_FOUND)

# ✅ Create an Outfit (User Selects Clothes)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outfit(request):
    """Allows users to create outfits manually by selecting items from their wardrobe"""
    serializer = OutfitSerializer(data=request.data)
    if serializer.is_valid():
        outfit = serializer.save(user=request.user)  # Associate with the user
        return Response(OutfitSerializer(outfit).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get All Outfits (User's Saved Outfits)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outfits(request):
    """Retrieves all outfits for the logged-in user"""
    outfits = Outfit.objects.filter(user=request.user)
    serializer = OutfitSerializer(outfits, many=True)
    return Response(serializer.data)

# ✅ AI Generates an Outfit (Basic API Placeholder)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_generate_outfit(request):
    """Allows AI to generate a full outfit (Placeholder API)"""
    # TODO: Integrate AI model (TensorFlow, OpenCV, or pre-trained API)
    return Response({'message': 'AI outfit generation coming soon!'}, status=status.HTTP_501_NOT_IMPLEMENTED)
# ✅ Plan an Outfit for a Date
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def plan_outfit(request):
    """Assigns an outfit to a calendar date"""
    serializer = OutfitPlannerSerializer(data=request.data)
    if serializer.is_valid():
        plan = serializer.save(user=request.user)
        return Response(OutfitPlannerSerializer(plan).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get All Planned Outfits (User's Calendar)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_planned_outfits(request):
    """Retrieves all planned outfits for the logged-in user"""
    plans = OutfitPlanner.objects.filter(user=request.user)
    serializer = OutfitPlannerSerializer(plans, many=True)
    return Response(serializer.data)
