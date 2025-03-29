from django.db import models
from django.contrib.auth.models import User  

# ✅ UserProfile Model (Extends Django's User model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female')]
    )
    modesty_preference = models.CharField(
        max_length=20, 
        choices=[('None', 'None'), ('Hijab-Friendly', 'Hijab-Friendly'), ('Modest', 'Modest')], 
        default='None'
    )
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ✅ Wardrobe Model (Stores User's Clothing)
class Wardrobe(models.Model):
    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
        ('All-Season', 'All-Season')  # For versatile clothing
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wardrobe_items")
    category = models.CharField(max_length=50)  # E.g., "Top", "Bottom", "Shoes"
    subcategory = models.CharField(max_length=50, blank=True, null=True)  # Optional
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    material = models.CharField(max_length=50)
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, default='All-Season')  # ✅ New Field
    tags = models.TextField(blank=True, null=True)  # Optional keywords
    photo_path = models.ImageField(upload_to="wardrobe/", blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.subcategory or 'General'} ({self.color}) [{self.season}]"


# ✅ Outfit Model (Stores User & AI-Generated Outfits)
class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfits")
    type = models.CharField(
        max_length=20, 
        choices=[('AI-generated', 'AI-generated'), ('User-created', 'User-created')]
    )
    selected_items = models.ManyToManyField(Wardrobe, related_name="outfit_items", blank=True)
    is_hijab_friendly = models.BooleanField(default=False)  # Used for filtering
    description = models.TextField(blank=True, null=True)
    photo_path = models.ImageField(upload_to="outfits/", blank=True, null=True)

    def __str__(self):
        return f"Outfit {self.pk} - {self.type}"


# ✅ OutfitPlanner Model (Schedules Outfits for Users)
class OutfitPlanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="planned_outfits")
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name="planned_dates")
    date = models.DateField()

    def __str__(self):
        return f"Planned Outfit {self.outfit.pk} for {self.date}" 