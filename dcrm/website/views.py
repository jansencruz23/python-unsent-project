from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Letter, User
from .utils import colors
from django.core.paginator import Paginator


def home(request):
    category = request.GET.get('category')
    query = request.GET.get('query')
    count = Letter.objects.count()

    if category == 'recipient':
        letters = Letter.objects.filter(recipient__icontains=query)
    elif category == 'message':
        letters = Letter.objects.filter(message__icontains=query)
    elif category == 'profile':
        letters = Letter.objects.filter(user__username__icontains=query, is_visible=True)
    else:
        letters = Letter.objects.all()

    paginator = Paginator(letters, 30)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
            return redirect('home')
    else:
        return render(request, 'home.html', {'letters': page_obj, 'count': count})


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
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def view_letter(request, pk):
    if request.user.is_authenticated:
        letter = Letter.objects.get(id=pk)
        username = User.objects.get(id=letter.user_id)
        current_user = request.user

        if letter.is_visible:
            return render(request, 'letter.html', {'letter': letter, 'username': username, 'current_user': current_user})
        else:
            return render(request, 'letter.html', {'letter': letter, 'username': 'Anonymous', 'current_user': current_user})
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
        return render(request, 'update_letter.html', {'form': form, 'colors': colors.color_mappings.items})
    else:
        messages.success(request, 'You must be logged in to update letter')
        return redirect('home')


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        letters = Letter.objects.filter(user_id=user.id)

        paginator = Paginator(letters, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'profile.html', {'letters': page_obj, 'user': user})
    else:
        messages.success(request, 'You must be logged in to view profile')
        return redirect('home')


def view_user(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        letters = Letter.objects.filter(user_id=pk, is_visible=True)

        paginator = Paginator(letters, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'view_user.html', {'letters': page_obj, 'user': user})
    else:
        messages.success(request, 'You must be logged in to view profile')
        return redirect('home')


def about(request):
    return render(request, 'about.html', {})
