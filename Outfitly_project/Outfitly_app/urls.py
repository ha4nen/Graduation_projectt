from django.urls import path
from .views import (register_user, login_user, get_user_profile, update_user_profile
    ,upload_clothing, get_wardrobe, update_clothing,
    create_outfit, get_outfits, ai_generate_outfit,
    plan_outfit, get_planned_outfits
)
urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('profile/<int:user_id>/', get_user_profile, name='get_user_profile'),
    path('profile/update/<int:user_id>/', update_user_profile, name='update_user_profile'),

  # Wardrobe APIs
    path('wardrobe/upload/', upload_clothing, name='upload_clothing'),
    path('wardrobe/', get_wardrobe, name='get_wardrobe'),
    path('wardrobe/update/<int:item_id>/', update_clothing, name='update_clothing'),

    # Outfit APIs
    path('outfits/create/', create_outfit, name='create_outfit'),
    path('outfits/', get_outfits, name='get_outfits'),
    path('outfits/ai-generate/', ai_generate_outfit, name='ai_generate_outfit'),

    # Outfit Planner APIs
    path('planner/', get_planned_outfits, name='get_planned_outfits'),
    path('planner/plan/', plan_outfit, name='plan_outfit'),
]
