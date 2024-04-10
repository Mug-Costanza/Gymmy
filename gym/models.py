from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
class CustomUser(AbstractUser):
    FITNESS_INTEREST_CHOICES = [
        ('weightlifting', 'Weightlifting'),
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('yoga', 'Yoga'),
    ]

    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()
    bodyweight = models.DecimalField(max_digits=5, decimal_places=2)
    weight_unit = models.CharField(max_length=3, choices=(('lbs', 'Pounds'), ('kg', 'Kilograms')))
    fitness_interests = models.CharField(max_length=20, choices=FITNESS_INTEREST_CHOICES, blank=True, null=True)
'''
    
class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
# Create your models here.
class UserProfile(models.Model):
    FITNESS_INTEREST_CHOICES = [
        ('weightlifting', 'Weightlifting'),
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('climbing', 'Climbing'),
        ('yoga', 'Yoga'),
    ]
    
    WEIGHT_UNIT_CHOICES = (
        ('lbs', 'Pounds'),
        ('kg', 'Kilograms'),
    )
    
    SEX_CHOICES = {
        ('Male', 'Male'),
        ('Female', 'Female'),
    }
    
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=None)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png', blank=True)
    sex = models.CharField(max_length=10, null=True, default=None)
    weight_unit = models.CharField(max_length=3, choices=WEIGHT_UNIT_CHOICES, default='kg')
    body_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_bench = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_deadlift = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_pullups = models.DecimalField(max_digits=5, decimal_places=0, null=True, default=None)
    pb_pushups = models.DecimalField(max_digits=5, decimal_places=0, null=True, default=None)
    pb_planktime = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_squat = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_miletime = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    pb_5ktime = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    daily_streak = models.PositiveIntegerField(default=0)
    fitness_interests = models.CharField(max_length=20, choices=FITNESS_INTEREST_CHOICES, blank=True, null=True)

    def increment_streak(self):
        self.daily_streak += 1
        self.save()

    def reset_streak(self):
        self.daily_streak = 0
        self.save()

class Workout(models.Model):

    WORKOUT_TYPES = [
        ('weightlifting', 'Weightlifting'),
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('climbing', 'Climbing'),
        ('rowing', 'Rowing'),
        ('combat', 'Combat'),
        ('yoga', 'Yoga'),
    ]
    
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=20, choices=WORKOUT_TYPES, blank=True, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=0, null=True, default=None)
    date = models.DateField(null = True)
    time = models.TimeField(null = True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type} on {self.date} at {self.time}, Location: {self.location}"

