from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        credential = authenticate(request, username=email, password=password)
        if credential is not None:
            user = CustomUser.objects.get(email=email)
            if user.is_authenticated:
                login(request, credential)
                return redirect('all_services')
        else:
            messages.success(request, 'Invalid Username/Password')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('all_services')

    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def edit_user(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    if request.method == 'POST' and request.user.is_merchant:
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update successfully')
            return redirect('settings')
    else:
        form = UserEditForm(instance=user)
    context = {
        'form': form,
        'user': user
        }
    return render(request, 'account_settings.html', context)


def reset_password_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.exists():
                # email_password_request.delay(user.pk)
                return redirect("reset_done")
    else:
        form = PasswordResetForm()
    context = {
           'form': form
       }
    return render(request, 'password_reset.html', context)


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully')
            # password_changed.delay(user.pk)
            return redirect('settings')

    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'account_settings.html', context)