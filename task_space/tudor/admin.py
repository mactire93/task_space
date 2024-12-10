from django.contrib import admin
from .models import AppUser, Task, ToDoItem, Note
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Task)
admin.site.register(ToDoItem)
admin.site.register(Note)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = AppUser

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)