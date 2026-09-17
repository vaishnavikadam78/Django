from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user=form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}!')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'users/logout.html')


@login_required(login_url='login')
def profile(request):
    return render(request,'users/profile.html')