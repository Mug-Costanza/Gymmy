from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Room, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import UserProfile
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import Workout
from .forms import WorkoutForm
from django.utils import timezone
import datetime
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import random
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

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
    
    def form_invalid(self, form):
        # Log or print form errors
        print("Form errors:", form.errors)
        return super().form_invalid(form)

class WorkoutUpdateView(UpdateView):
    model = Workout
    form_class = WorkoutForm
    success_url = '/calendar/'  # Redirect to the calendar view after update
    
class WorkoutDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        workout = get_object_or_404(Workout, pk=pk)
        workout.delete()
        return redirect('profile', pk=request.user.profile.pk)  # Redirect to the profile page after deletion
        
def convert_if_not_none(value, conversion_factor):
    return value * conversion_factor if value is not None else None

class profileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        weight_unit = profile.weight_unit  # Accessing directly from profile object
        
        # workouts = profile.workout_set.all().order_by('-date')  # Ordering workouts by date in descending order
        # Fetch workouts in descending order of date
        workout_list = profile.workout_set.all().order_by('-date')

        # Create a paginator object
        paginator = Paginator(workout_list, 5)  # Show 5 workouts per page
        page_number = request.GET.get('page')
        workouts = paginator.get_page(page_number)
        
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
            'form': WorkoutForm(initial={'day': current_date.day,
                                          'month': current_date.month,
                                          'year': current_date.year}),
            'workouts': workouts,
            'daily_streak': profile.daily_streak,
        }

        return render(request, 'profile.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = WorkoutForm(request.POST)
        
        # Inside your view or form handling code
        if form.is_valid():
            cleaned_data = form.cleaned_data
            month = int(cleaned_data['month'])
            day = int(cleaned_data['day'])
            year = int(cleaned_data['year'])
    
            # Create a datetime object with no specific time (defaults to midnight)
            combined_datetime = datetime.datetime(year, month, day)
    
            # Make the datetime object timezone-aware
            aware_datetime = make_aware(combined_datetime)
            
            # Now 'date' field contains the correct combined date value
            form = WorkoutForm(cleaned_data)
            
            # Save the form with the current user's profile
            workout = form.save(commit=False)
            workout.profile_id = pk  # Associate with the correct profile
            workout.save()
            
            # Increment daily streak for the user's profile
            profile = get_object_or_404(UserProfile, pk=pk)
            profile.increment_streak()
            
            return redirect('profile', pk=pk)
        else:
            print(form.errors)  # Add this line to print form errors
            profile = get_object_or_404(UserProfile, pk=pk)
            workouts = profile.workout_set.all()
            context = {
                'profile': profile,
                'form': form,
                'workouts': workouts,
                'weight_unit': profile.weight_unit,
                'pb_bench': profile.pb_bench,
                'pb_deadlift': profile.pb_deadlift,
                'pb_squat': profile.pb_squat,
                'pb_pullups': profile.pb_pullups,
                'pb_pushups': profile.pb_pushups,
                'pb_planktime': profile.pb_planktime,
                'pb_miletime': profile.pb_miletime,
                'pb_5ktime': profile.pb_5ktime,
                'daily_streak': profile.daily_streak,
            }
        
            return render(request, 'profile.html', context)  # Render the page with errors instead of redirecting

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly set the backend attribute to the backend you want to use.
            # The backend string should match one of the backends listed in AUTHENTICATION_BACKENDS in your settings.py.
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to homepage URL or appropriate URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
    
def logoutView(request):
    logout(request)
    return redirect('home')  # Assuming 'home' is the name of your homepage URL

#chats
def chat_home(request):
    return render(request, "chat_home.html")


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })

def checkview(request):
    user = request.user
    friends = user.profile.friends.all()
    username = request.GET.get('friend_user')
    name = request.GET.get('username')
    # Ensure usernames is a list
    usernames_list = [username, name]

    # Sort the list of usernames
    sorted_usernames = sorted(usernames_list)

    # Construct the URL with the sorted usernames
    room_url = sorted_usernames[0] + sorted_usernames[1]

    room = request.GET.get('room')
    username = request.GET.get('username')

    if not room_url:
        return HttpResponseBadRequest("Room name cannot be empty")

    if Room.objects.filter(name=room_url).exists():
        return redirect('/'+room_url)
    else:
        new_room = Room.objects.create(name=room_url)
        return redirect('/'+room_url)

    return render(request, 'my_template.html', {'sorted_usernames': sorted_usernames, 'room_url': room_url})
    

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})

def contact_view(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback', '')
        email = request.POST.get('email', '')

        # Send email
        send_mail(
            subject="Received contact form submission",
            message=feedback,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        # Render the same page with a success message
        return render(request, 'contact.html', {'success': True})
    return render(request, 'find_trainer.html', {'success': False})
