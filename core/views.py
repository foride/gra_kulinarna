from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, Sum, Value
from django.db.models.fields import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserAchievement, Visit, Achievement, Venue, Discussion, Ranking
from django.db.models.functions import Coalesce
from django.db.models import Max


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['confirm-password']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
    else:
        return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard_view(request):
    user = request.user

    # Fetch achievements count for the user
    achievements_count = UserAchievement.achievements_count_for_user(user)

    # Fetch total achievements
    total_achievements = Achievement.total_achievements_count()

    # Fetch user ranking
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_ranking = user_profile.user_ranking()
    except UserProfile.DoesNotExist:
        user_ranking = UserProfile.objects.count()  # Default rank if user profile doesn't exist

    # Assuming you have a logic to get the recommended place
    recommended_place = "Efes Kebab Warszawa"  # Placeholder

    context = {
        'achievements_count': achievements_count,
        'total_achievements': total_achievements,
        'user_ranking': user_ranking,
        'recommended_place': recommended_place,
    }

    return render(request, 'dashboard.html', context)


@login_required
def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Venue.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'search.html', context)


@login_required
def venue_details_view(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    discussions = Discussion.objects.filter(venue=venue)

    context = {
        'venue': venue,
        'discussions': discussions,
    }

    return render(request, 'venue details.html', context)


@login_required
def verify_venue_code(request, venue_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        entered_code = request.POST.get('venue_code')
        venue = get_object_or_404(Venue, id=venue_id)

        if entered_code == venue.visit_code:
            ranking, created = Ranking.objects.get_or_create(user=request.user, defaults={'points': 0})
            if created:
                max_position = Ranking.objects.aggregate(Max('position'))['position__max']
                ranking.position = max_position + 1 if max_position is not None else 1
            ranking.points += 50
            ranking.save()
            return JsonResponse({'status': 'success', 'message': 'Poprawny kod! Otrzymujesz 50 punktów.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Niepoprawny kod.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@login_required
def add_review(request, venue_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        venue = get_object_or_404(Venue, id=venue_id)
        discussion = Discussion.objects.create(user=request.user, venue=venue, content=content)
        return redirect('venue_details', venue_id=venue.id)


@login_required
def user_profile_view(request):
    user = request.user

    # Fetch user points
    total_points = UserAchievement.objects.filter(user=user).aggregate(Sum('achievement__points_required'))[
                       'achievement__points_required__sum'] or 0

    # Fetch visited venues count
    visited_venues_count = Visit.objects.filter(user=user).count()

    # Fetch achievements count
    achievements_count = UserAchievement.objects.filter(user=user).count()

    # Fetch user profile
    user_profile = UserProfile.objects.get(user=user)

    # Fetch favorite venues
    favorite_venues = user_profile.favorite_venues.all()

    # Fetch available venues for adding to favorites
    available_venues = Venue.objects.exclude(id__in=favorite_venues.values_list('id', flat=True))

    context = {
        'total_points': total_points,
        'visited_venues_count': visited_venues_count,
        'achievements_count': achievements_count,
        'favorite_venues': favorite_venues,
        'available_venues': available_venues,
    }

    return render(request, 'user profile.html', context)


@login_required
def add_favorite(request):
    if request.method == 'POST':
        venue_id = request.POST.get('venue')
        venue = Venue.objects.get(id=venue_id)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.favorite_venues.add(venue)
        return redirect('user_profile')


@login_required
def remove_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        venue_id = data.get('venue_id')
        venue = Venue.objects.get(id=venue_id)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.favorite_venues.remove(venue)
        return JsonResponse({'success': True})


@login_required
def user_ranking_view(request):
    # Subquery to get points from the Ranking model
    ranking_points_subquery = Ranking.objects.filter(user=OuterRef('user')).values('points')

    # Annotate user profiles with their total points using Subquery and Coalesce to handle users without points
    user_profiles = UserProfile.objects.annotate(
        total_points=Coalesce(Subquery(ranking_points_subquery[:1]), Value(0))
    ).order_by('-total_points')

    # Calculate visited venues count
    for user_profile in user_profiles:
        user_profile.visited_venues_count = user_profile.total_points // 50

    context = {
        'user_profiles': user_profiles,
    }

    return render(request, 'user ranking.html', context)


@login_required
def achievements_view(request):
    user = request.user
    achieved_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')

    context = {
        'achieved_achievements': achieved_achievements,
    }

    return render(request, 'achievements.html', context)


@login_required
def password_change_view(request):
    return render(request, 'achievements.html')
