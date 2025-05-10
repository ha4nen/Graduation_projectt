from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')]
    )
    
    modesty_preference = models.CharField(
        max_length=20,
        choices=[
            ('None', 'None'),
            ('Hijab-Friendly', 'Hijab-Friendly')
        ],
        default='None'
    )
    
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # New fields
    bio = models.TextField(blank=True, null=True, max_length=500)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ✅ Category & SubCategory Models
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"


# ✅ Wardrobe Model
class Wardrobe(models.Model):
    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
        ('All-Season', 'All-Season'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wardrobe_items")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    material = models.CharField(max_length=50)
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, default='All-Season')
    tags = models.TextField(blank=True, null=True)
    photo_path = models.ImageField(upload_to="wardrobe/", blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.subcategory or 'General'} ({self.color}) [{self.season}]"


# ✅ Outfit Model
class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfits")
    type = models.CharField(
        max_length=20,
        choices=[('AI-generated', 'AI-generated'), ('User-created', 'User-created')]
    )
    selected_items = models.ManyToManyField(Wardrobe, related_name="outfit_items", blank=True)
    is_hijab_friendly = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    photo_path = models.ImageField(upload_to="outfits/", blank=True, null=True)
      # ✅ New additions
    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
        ('All-Season', 'All-Season'),
    ]
    season = models.CharField(max_length=15, choices=SEASON_CHOICES, default='All-Season')
    tags = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Outfit {self.pk} - {self.type}"


# ✅ Outfit Planner Model
class OutfitPlanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="planned_outfits")
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name="planned_dates")
    date = models.DateField()

    def __str__(self):
        return f"Planned Outfit {self.outfit.pk} for {self.date}"


# ✅ Post Model (Feed)
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at.date()}"


# ✅ Like Model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


# ✅ Follow Model
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
