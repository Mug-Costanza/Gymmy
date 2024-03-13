from django.urls import path
from .views import index, about, calendar, findPartner, findTrainer, profileView, loginView, registerView, logoutView
from .views import CalendarView, WorkoutCreateView, WorkoutUpdateView, localGyms

urlpatterns = [
    path('', index, name='index'),
    path('', index, name='home'),
    path('post', index, name='post-detail'),
    path('profile/<int:pk>/', profileView.as_view(), name='profile'),
    path('about', about, name='about'),
    path('find-partner', findPartner.as_view(), name='find-partner'),
    path('find-trainer', findTrainer.as_view(), name='find-trainer'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('local-gyms/', localGyms, name='local-gyms'),
    path('workout/add/', WorkoutCreateView.as_view(), name='workout-add'),
    path('workout/edit/<int:pk>/', WorkoutUpdateView.as_view(), name='workout-edit'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),
    path('register', registerView, name='register')
]
