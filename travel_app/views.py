from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .form import SignupForm  
from .models import Profile

from django.contrib import messages  

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Save profile information
            Profile.objects.create(
                user=user,
                country_code=form.cleaned_data['country_code'],
                phone_number=form.cleaned_data['phone_number']
            )

            messages.success(request, 'You have signed up successfully. Please log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def profile(request):
    context = {}
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            context['profile'] = profile
        except Profile.DoesNotExist:
            profile = None  # User doesn't have a profile yet
            messages.warning(request, "Profile not found. Please complete your profile.")
        context.update({
            'user': request.user,
            'profile': profile,
        })
    else:
        # User is not logged in, still show the page without details
        messages.info(request, "Please log in to see profile details.")

    return render(request, 'profile.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('landing')

def landing(request):
    return render(request, 'landing.html')

def explore(request):
    return render(request, 'explore.html')

def packages(request):
    return render(request, 'packages.html')

from django.http import JsonResponse

def bookings(request):
    if request.method == "POST":
        # Extract form data (assume AJAX submission for real-time updates)
        package = request.POST.get('package')
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        preferences = request.POST.get('preferences')

        # Validate and process data
        if package and name and email and date:
            # Mocked booking options response
            options = [
                f"Option 1: {package} - {date}",
                f"Option 2: Discounted Package - {package}",
            ]
            return JsonResponse({'success': True, 'options': options})
        return JsonResponse({'success': False, 'message': "Please fill in all fields!"})

    # Render the page for GET requests
    return render(request, 'bookings.html')


def bookings_redirect(request):
    messages.warning(request, "Please log in to access the bookings page.")
    return redirect('login')  # Assuming your login URL name is 'login'

def contact(request):
    return render(request, 'contact.html')

def terms_conditions(request):
    return render(request, 'terms.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')  # Redirect to the profile page after saving

    return redirect('profile')  # Redirect if the method is not POST

