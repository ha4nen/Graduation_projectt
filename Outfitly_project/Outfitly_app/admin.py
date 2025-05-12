from django.contrib import admin
from .models import Category, Follow, Like, Post, SubCategory, UserProfile, Wardrobe, Outfit, OutfitPlanner

# Register your models here
admin.site.register(UserProfile)
admin.site.register(Wardrobe)
admin.site.register(Outfit)
admin.site.register(OutfitPlanner)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)

from django.contrib import admin

# Register your models here.
