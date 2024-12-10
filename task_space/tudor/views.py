from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, ToDoItem, Note, AppUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ToDoForm, NoteForm, TaskForm, UpdateUserForm, ChangePasswordForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import datetime
# Exceptions:
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(task_user=request.user.id)
        return render(request, 'home.html', {'tasks': tasks})
    else:
        return redirect('login')

def finished_tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(task_user=request.user.id)
        return render(request, 'finished_tasks.html', {'tasks': tasks})
    else:
        return redirect('login')

def about(request):
    return render(request, 'about.html', {})

def view_profile(request):
    if request.user.is_authenticated:
        app_user = AppUser.objects.get(user=request.user)
        user = request.user
        print(app_user)
        return render(request, 'view_profile.html',
                      {
                          'app_user': app_user,
                          'user': user
                      })
    else:
        return redirect('login')


def edit_task(request, pk):
    if request.user.is_authenticated:
        try:
            task_model = Task._meta
            task_max_char = task_model.get_field('description').max_length
            title_max_char = task_model.get_field('title').max_length
            app_user = AppUser.objects.get(user=request.user)
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the task does not exist!"))
            return redirect('home')
        if request.user.id == task.task_user.id:
            form = TaskForm(request.POST or None, instance=task)
            if request.method == "POST":
                if form.is_valid():
                    task = form.save(commit=False)
                    task.task_user_id = app_user.user.id
                    task.save()
                    messages.success(request, ("Your task has been edited!"))
                    return redirect('home')
        return render(request, 'edit_task.html',
                      {
                          'form': form,
                          'task': task,
                          'task_max_char': task_max_char,
                          'title_max_char': title_max_char
                      })
    else:
        return redirect('login')

def delete_item(request, pk, item_id):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
            todo_item = ToDoItem.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the item does not exist!"))
            return redirect('view_task', pk=task.id)

        if request.user.id == task.task_user.id:
            todo_item.delete()
            messages.success(request, ("The item has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect(request.META.get("HTTP_REFERER"))

def edit_note(request, pk, note_id):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
            note = Note.objects.get(pk=note_id)
            note_model = Note._meta
            note_max_characters = note_model.get_field('body').max_length
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the note does not exist!"))
            return redirect('view_task', pk=task.id)
        if request.user.id == task.task_user.id:
            note_form = NoteForm(request.POST or None, instance=note)
            if request.method == "POST":
                if note_form.is_valid():
                    note = note_form.save(commit=False)
                    note.task_id = task.id
                    note.created_at = datetime.datetime.now()
                    note.save()
                    messages.success(request, ("Your note has been edited!"))
                    return redirect('view_task', pk=task.id)
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
        return render(request, 'edit_note.html',
                      {
                          'note_form': note_form,
                          'note': note,
                          'note_max_characters': note_max_characters
                      })



def delete_note(request, note_id, pk):
    """ takes the id of the note and the id of the task
    (template view_task -> notes -> url note.id task.id)
    then queries the db and returns a specific object
    checks if the task belongs to the logged in user and removes the note """
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
            note = Note.objects.get(pk=note_id)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the note does not exist!"))
            return redirect('view_task', pk=task.id)
        if request.user.id == task.task_user.id:
            note.delete()
            messages.success(request, ("The note has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')

    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect(request.META.get("HTTP_REFERER"))

def return_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the task does not exist!"))
            return redirect('home')
        if request.user.id == task.task_user.id:
            task.is_done = False
            task.save()
            messages.success(request, ("The task has been returned!"))
            return redirect('home')
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect(request.META.get("HTTP_REFERER"))

def finish_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the task does not exist!"))
            return redirect('home')
        if request.user.id == task.task_user.id:
            task.is_done = True
            task.save()
            messages.success(request, ("The task has been finished!"))
            return redirect('finished_tasks')
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect(request.META.get("HTTP_REFERER"))


def delete_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the task does not exist!"))
            return redirect('home')
        if request.user.id == task.task_user.id:
            task.delete()
            messages.success(request, ("The task has been deleted!"))
            return redirect('home')
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect(request.META.get("HTTP_REFERER"))




def add_task(request):
    if request.user.is_authenticated:
        task_model = Task._meta
        task_max_char = task_model.get_field('description').max_length
        title_max_char = task_model.get_field('title').max_length
        app_user = AppUser.objects.get(user=request.user)
        form = TaskForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                task = form.save(commit=False)
                task.task_user_id = app_user.user.id
                task.save()
                messages.success(request, ("Your task has been added!"))
                return redirect('home')
        return render(request, 'add_task.html',
                      {
                          'form': form,
                          'task_max_char': task_max_char,
                          'title_max_char': title_max_char
                      })
    else:
        return redirect('login')



def check_boxes(request):
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item = get_object_or_404(ToDoItem, id=item_id)
        if item.item_done:
            print("Przed:", item.item_done)
            item.item_done = False
            item.save()
            print("Po:", item.item_done)
        else:
            print("Przed:", item.item_done)
            item.item_done = True
            item.save()
            print("Po:", item.item_done)

        response = JsonResponse({'item': item.item_done,
                                 'item_id': item_id
                                 })
    return response

def view_task(request, pk):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            messages.success(request, ("An error has occurred, the task does not exist!"))
            return redirect('home')
        list_items = ToDoItem.objects.filter(task=task.id)
        notes = Note.objects.filter(task=task.id)
        note_model = Note._meta
        note_max_characters = note_model.get_field('body').max_length
        todo_model = ToDoItem._meta
        todo_max_char = todo_model.get_field('title').max_length


        form = ToDoForm(request.POST or None)
        note_form = NoteForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                to_do_item = form.save(commit=False)
                to_do_item.task_id = task.id
                to_do_item.save()
                messages.success(request,("Your Item has been added!"))
                return redirect(request.META.get("HTTP_REFERER"))

        if request.method == "POST":
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.task_id = task.id
                note.save()
                messages.success(request, ("Your note has been added!"))
                return redirect(request.META.get("HTTP_REFERER"))

        if request.user.id == task.task_user.id:
            return render(request, 'view_task.html', {
                'task': task,
                'list_items': list_items,
                'notes': notes,
                'form': form,
                'note_form': note_form,
                'note_max_characters': note_max_characters,
                'todo_max_char': todo_max_char
            })
        else:
            messages.success(request, ("No authorisation!"))
            return redirect('home')
    else:
        messages.success(request, ("You have to be logged in!"))
        return redirect('login')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # log in user
            user = authenticate(username=username, password=password)

            # automatically fill in the profile AppUser
            app_user = AppUser.objects.get(user=user)
            app_user.first_name = form.cleaned_data['first_name']
            app_user.last_name = form.cleaned_data['last_name']
            app_user.email = form.cleaned_data['email']
            app_user.save()

            login(request, user)
            messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
            return redirect('home')
        else:
            messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def edit_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        app_user = AppUser.objects.get(user=current_user)
        form = UpdateUserForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            app_user.first_name = form.cleaned_data['first_name']
            app_user.last_name = form.cleaned_data['last_name']
            app_user.email = form.cleaned_data['email']
            app_user.save()

            login(request, current_user)
            messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
            return redirect('home')
        return render(request, 'edit_profile.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect('edit_profile')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect('home')

