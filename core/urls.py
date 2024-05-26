from django.urls import path
from core import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('search/', views.search_view, name='search'),
    path('venue details/', views.venue_details, name='venue_details'),
    path('user profile/', views.user_profile, name='user_profile'),
    path('user ranking/', views.user_ranking, name='user_ranking'),
    path('achievements/', views.achievements, name='achievements'),
]