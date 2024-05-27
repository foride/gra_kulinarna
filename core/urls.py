from django.urls import path
from core import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('venue-details/', views.venue_details_view, name='venue_details'),
    path('venue/<int:venue_id>/', views.venue_details_view, name='venue_details'),
    path('venue/<int:venue_id>/add_review/', views.add_review, name='add_review'),
    path('venue/<int:venue_id>/verify_code/', views.verify_venue_code, name='verify_venue_code'),
    path('user-profile/', views.user_profile_view, name='user_profile'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('password_change/', views.password_change_view, name='password_change'),
    path('remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('user-ranking/', views.user_ranking_view, name='user_ranking'),
    path('achievements/', views.achievements_view, name='achievements'),
]
