from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddLetterForm
from .models import Letter, User, Notification
from .templatetags import colors
from django.core.paginator import Paginator


def home(request):
    category = request.GET.get('category')
    query = request.GET.get('query')

    letters = Letter.objects.all().order_by('-created_at')
    if query:
        if category == 'recipient':
            letters = letters.filter(recipient__icontains=query)
        elif category == 'message':
            letters = letters.filter(message__icontains=query)
        elif category == 'profile':
            letters = Letter.objects.filter(user__username__icontains=query, is_visible=True)

    paginator = Paginator(letters, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_username = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_username, is_read=False)
    count = letters.count()

    return render(request, 'home.html', {
        'letters': page_obj,
        'count': count,
        'notifications': notifications
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')

    return render(request, 'login_user.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome')
            return redirect('home')

    return render(request, 'register.html', {'form': form})


def view_letter(request, pk):
    if request.user.is_authenticated:
        letter = Letter.objects.get(id=pk)
        displayed_user = letter.user.username if letter.is_visible and letter.user else 'Anonymous'
        current_user = request.user
        notifications = Notification.objects.filter(letter__recipient__iexact=current_user.username, is_read=False)

        return render(request, 'letter.html', {
            'letter': letter,
            'username': displayed_user,
            'current_user': current_user,
            'notifications': notifications
        })
    else:
        messages.success(request, 'You must be logged in to view a letter')
        return redirect('home')


def letter_notif(request, pk):
    if request.user.is_authenticated:
        letter = Letter.objects.get(id=pk)
        current_user = request.user
        displayed_username = letter.user.username if letter.is_visible and letter.user else 'Anonymous'

        notifications = Notification.objects.filter(letter__recipient__iexact=current_user.username, is_read=False)
        notification = Notification.objects.get(letter__id=pk)
        notification.is_read = True
        notification.save()

        return render(request, 'letter.html', {
            'letter': letter,
            'username': displayed_username,
            'current_user': current_user,
            'notifications': notifications
        })
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
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to add a letter')
        return redirect('login_user')

    form = AddLetterForm(request.POST or None)
    current_user = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)

    if request.method == 'POST' and form.is_valid():
        letter = form.save(commit=False)
        letter.user = request.user
        letter.save()
        messages.success(request, 'Letter is submitted')

        Notification.objects.create(letter=letter, is_read=False)
        return redirect('home')

    return render(request, 'add_letter.html', {
        'form': form,
        'colors': colors.color_mappings.items,
        'notifications': notifications
    })


def update_letter(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to update a letter')
        return redirect('home')

    current_letter = Letter.objects.get(id=pk)
    form = AddLetterForm(request.POST or None, instance=current_letter)

    if form.is_valid():
        form.save()
        messages.success(request, 'Letter has been updated')

        notification = Notification.objects.get(letter__id=pk)
        notification.is_read = False
        notification.save()

        return redirect('home')

    current_user = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)

    return render(request, 'update_letter.html', {
        'form': form,
        'colors': colors.color_mappings.items,
        'notifications': notifications
    })


def profile(request):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to view profile')
        return redirect('home')

    user = request.user
    letters = Letter.objects.filter(user_id=user.id).order_by('-created_at')
    count = letters.count()

    current_user = user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)

    paginator = Paginator(letters, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profile.html', {
        'letters': page_obj,
        'user': user,
        'count': count,
        'notifications': notifications
    })


def view_user(request, pk):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to view profile')
        return redirect('home')

    user = User.objects.get(id=pk)
    letters = Letter.objects.filter(user_id=pk, is_visible=True).order_by('-created_at')
    count = letters.count()

    current_user = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)

    paginator = Paginator(letters, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'view_user.html', {
        'letters': page_obj,
        'user': user,
        'count': count,
        'notifications': notifications
    })


def about(request):
    return render(request, 'about.html', {})


def mailbox(request):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to view your mailbox')
        return redirect('login_user')

    user = request.user
    letters = Letter.objects.filter(recipient__iexact=user.username).order_by('-created_at')
    count = letters.count()

    current_user = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)

    paginator = Paginator(letters, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mailbox.html', {
        'letters': page_obj,
        'user': user,
        'count': count,
        'notifications': notifications
    })


def clear_notif(request):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to clear notifications')
        return redirect('login_user')

    current_user = request.user.username
    notifications = Notification.objects.filter(letter__recipient__iexact=current_user, is_read=False)
    notifications.update(is_read=True)

    messages.success(request, 'Notifications have been cleared')
    return redirect('home')
