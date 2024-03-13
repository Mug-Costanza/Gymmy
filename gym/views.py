from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import UserProfile
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import Workout
from .forms import WorkoutForm
from django.utils import timezone
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
    
class findPartner(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'find_partner.html')
        
class findTrainer(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'find_trainer.html')
    
def calendar(request):
    return render(request, 'calendar.html')
    
def localGyms(request):
    return render(request, 'local_gyms.html')
    
class CalendarView(TemplateView):
    template_name = 'calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workouts'] = Workout.objects.all()
        return context

class WorkoutCreateView(CreateView):
    model = Workout
    form_class = WorkoutForm
    success_url = '/calendar/'  # Redirect to the calendar view after creation

class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    success_url = '/calendar/'  # Redirect to the calendar view after update

def convert_if_not_none(value, conversion_factor):
    return value * conversion_factor if value is not None else None

class profileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        weight_unit = profile.weight_unit  # Accessing directly from profile object
        
        workouts = profile.workout_set.all()  # Accessing workouts using reverse relationship
        
        current_date = date.today()

        # Pass default date value to the form
        context = {
            'user': profile.user,
            'profile': profile,
            'weight_unit': weight_unit,
            'pb_bench': profile.pb_bench,
            'pb_deadlift': profile.pb_deadlift,
            'pb_squat': profile.pb_squat,
            'pb_pullups': profile.pb_pullups,
            'pb_pushups': profile.pb_pushups,
            'pb_planktime': profile.pb_planktime,
            'pb_miletime': profile.pb_miletime,
            'pb_5ktime': profile.pb_5ktime,
            'form': WorkoutForm(initial={'date': current_date}),
            'workouts': workouts,
            'daily_streak': profile.daily_streak,
        }

        return render(request, 'profile.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = WorkoutForm(request.POST)
        
        if form.is_valid():
            # Save the form with the current user's profile
            workout = form.save(commit=False)
            workout.profile_id = pk  # Associate with the correct profile
            workout.save()
            
            # Increment daily streak for the user's profile
            profile = get_object_or_404(UserProfile, pk=pk)
            profile.increment_streak()
            
            return redirect('profile', pk=pk)
        else:
            # Retrieve the profile again as done in the get method
            profile = get_object_or_404(UserProfile, pk=pk)
            workouts = profile.workout_set.all()
            context = {
                'profile': profile,
                'form': form,
                'workouts': workouts
            }
            return redirect('calendar')
            
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Assuming 'home' is the name of your homepage URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # If you have additional actions, like creating a user profile, add them here
            login(request, user)  # Log the user in
            return redirect('home')  # Assuming 'home' is the name of your homepage URL
    else:
        form = UserCreationForm()
        # If you need to pass extra context to your form (like a years range for a date_of_birth field), ensure your form supports it.
    return render(request, 'register.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('home')  # Assuming 'home' is the name of your homepage URL
