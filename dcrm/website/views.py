from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Letter
from .utils import colors
from django.db.models import Q


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, 'An error occurred. Try again')
            
    letters = Letter.objects.filter(Q(is_visible=True) | Q(user_id=request.user.id))
    return render(request, 'home.html', {'letters': letters})


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome')

            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form': form})


def view_letter(request, pk):
    if request.user.is_authenticated:
        letter = Letter.objects.get(id=pk)
        return render(request, 'letter.html', {'letter': letter})
    else:
        messages.success(request, 'You must be logged in to view a letter')
        return redirect('home')


def delete_letter(request, pk):
    if request.user.is_authenticated:
        deleted_it = Letter.objects.get(id=pk)
        deleted_it.delete()
        messages.success(request, 'Letter deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to view a letter')
        return redirect('home')


def add_letter(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                letter = form.save(commit=False)
                letter.user = request.user
                letter.save()
                messages.success(request, 'Letter is submitted')
                return redirect('home')
        return render(request, 'add_letter.html', {'form': form, 'colors': colors.color_mappings.items})
    else:
        messages.success(request, 'You must be logged in to add letter')
        return redirect('home')


def update_letter(request, pk):
    if request.user.is_authenticated:
        current_letter = Letter.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_letter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Letter has been updated')
            return redirect('home')
        return render(request, 'update_letter.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to update letter')
        return redirect('home')


