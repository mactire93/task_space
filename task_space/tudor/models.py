from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Create your models here.

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __str__(self):
        """ return object name """
        return self.user.username

# Create a user Profile (AppUser) by default when user sings up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = AppUser(user=instance)
        user_profile.save()

# automate the profile thing
post_save.connect(create_profile, sender=User)


class Task(models.Model):
    task_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    date = models.DateField(default=datetime.datetime.today)
    image = models.ImageField(upload_to='uploads/task/', blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        """ return object name"""
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_done = models.BooleanField(default=False)

    def __str__(self):
        """return object name"""
        return self.title

class Note(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
