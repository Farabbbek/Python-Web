
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from authapp.models import Contact,Profile
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import FoodLog
from .forms import FoodLogForm
from .models import WorkoutSet,ExerciseHistory
from .forms import WorkoutSetForm
from django.db.models.functions import TruncMonth
import json
from django.db.models import Max, Count, Q
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
import random
import string
from django.utils import timezone
from django.contrib.auth.hashers import make_password
# Create your views here.
def Home(request):
    return render(request, 'index.html')

def register(request):
   if request.method=="POST":
        usernumber=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        if pass1!=pass2:
            messages.info(request,"Password is not Matching")
            return redirect('/register')
       
        try:
            if User.objects.get(usernumber=usernumber):
                messages.warning(request,"Phone Number is Taken")
                return redirect('/register')
           
        except Exception as identifier:
            pass
        
        
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/register')
           
        except Exception as identifier:
            pass
        
        myuser=User.objects.create_user(usernumber,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/login')
   
   return render(request,"register.html")

def handlelogin(request):
    if request.method == "POST":        
        email = request.POST.get('email')  # Use email instead of username
        pass1 = request.POST.get('pass1')
        
        # Try to authenticate the user by email
        myuser = authenticate(request, username=email, password=pass1)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
        
    return render(request, "handlelogin.html")

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('num')
        desc = request.POST.get('desc')
        
        # Save the contact form to the database (using the Contact model)
        myquery = Contact(name=name, email=email, phonenumber=number, desc=desc)
        myquery.save()

        # Telegram notification
        bot_token = "7971753075:AAHaQWpQDJavJ11Nb5OhYi7mOTxYxXOjMNo"
        chat_id = "916328410"
        message = f"New Contact Submission\n\nName: {name}\nEmail: {email}\nPhone: {number}\nMessage: {desc}"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)  # Sends the message to your Telegram account
    # Display a message to the user
        messages.info(request, "We appreciate you getting in touch. Our team will get back to you soon.")
        return redirect('/contact')
        
    return render(request, "contact.html")


@login_required
def profile(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        email = request.POST.get('email')  # Email should be editable

        # Get or create the profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        # Ensure that username (phone) does not conflict with existing usernames
        if phone != request.user.username:
            # Check if the new phone number is already taken
            if User.objects.filter(username=phone).exists():
                messages.error(request, "This phone number is already in use by another user.")
                return redirect('/profile')
            else:
                request.user.username = phone  # Update username to the new phone number
                request.user.save()

        # Update the user information (like email and phone)
        request.user.email = email  # Update the email
        request.user.save()  # Save the updated user data

        # Update the profile fields
        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone = phone
        profile.bio = bio

        avatar = request.FILES.get('avatar')
        if avatar:
            profile.avatar = avatar
        
        profile.save()  # Save the profile data

        messages.success(request, 'Profile updated successfully!')
        return redirect('/profile')

    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {'profile': profile}
    return render(request, "profile.html", context)

@login_required
def food_log_list(request):
    food_logs = FoodLog.objects.filter(user=request.user).order_by('-date', '-time')
    context = {
        'food_logs': food_logs,
    }
    return render(request, 'food_log.html', context)

@login_required
def food_log_create(request):
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = request.user
            food_log.save()
            messages.success(request, 'Food log created successfully!')
            return redirect('food_log_list')
    else:
        form = FoodLogForm()
    
    return render(request, 'food_log_form.html', {'form': form, 'action': 'Create'})

@login_required
def food_log_edit(request, pk):
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FoodLogForm(request.POST, instance=food_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food log updated successfully!')
            return redirect('food_log_list')
    else:
        form = FoodLogForm(instance=food_log)
    
    return render(request, 'food_log_form.html', {
        'form': form,
        'action': 'Edit',
        'food_log': food_log
    })

@login_required
def food_log_delete(request, pk):
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            food_log.delete()
            messages.success(request, 'Food log deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting food log: {str(e)}')
    
    return redirect('food_log_list')


@login_required
def workout_set_list(request):
    sets = WorkoutSet.objects.filter(user=request.user)
    return render(request, 'workout_sets.html', {'sets': sets})

@login_required
def workout_set_create(request):
    if request.method == 'POST':
        exercise_names = request.POST.getlist('exercise_name[]')
        weights = request.POST.getlist('weight[]')
        reps = request.POST.getlist('reps[]')
        sets = request.POST.getlist('sets[]')
        notes = request.POST.getlist('notes[]')
        day_of_week = request.POST.get('day_of_week')
        
        # Create workout sets for each exercise
        for i in range(len(exercise_names)):
            WorkoutSet.objects.create(
                user=request.user,
                exercise_name=exercise_names[i],
                weight=weights[i],
                reps=reps[i],
                sets=sets[i],
                day_of_week=day_of_week,
                notes=notes[i] if notes[i] else None
            )
        
        messages.success(request, 'Workout sets added successfully!')
        return redirect('workout_set_list')
    
    context = {
        'action': 'Create',
        'days_of_week': WorkoutSet.DAYS_OF_WEEK
    }
    return render(request, 'workout_set_form.html', context)

@login_required
def workout_set_edit(request, pk):
    workout_set = get_object_or_404(WorkoutSet, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutSetForm(request.POST, instance=workout_set)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout set updated successfully!')
            return redirect('workout_set_list')
    else:
        form = WorkoutSetForm(instance=workout_set)
    return render(request, 'workout_set_form.html', {'form': form, 'action': 'Edit'})

@login_required
def workout_set_delete(request, pk):
    workout_set = get_object_or_404(WorkoutSet, pk=pk, user=request.user)
    if request.method == 'POST':
        workout_set.delete()
        messages.success(request, 'Workout set deleted successfully!')
        return redirect('workout_set_list')
    return render(request, 'workout_set_confirm_delete.html', {'workout_set': workout_set})


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@login_required
def exercise_progress(request):
    # Get unique exercises from history
    exercises = ExerciseHistory.objects.filter(user=request.user).values_list(
        'exercise_name', flat=True).distinct()
    
    progress_data = {}
    for exercise in exercises:
        # Get monthly progress including personal records
        monthly_data = ExerciseHistory.objects.filter(
            user=request.user,
            exercise_name=exercise
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            max_weight=Max('weight'),
            pr_count=Count('id', filter=Q(personal_record=True))
        ).order_by('month')
        
        # Format data for charts
        progress_data[exercise] = {
            'labels': [data['month'].strftime('%B %Y') for data in monthly_data],
            'weights': [float(data['max_weight']) for data in monthly_data],
            'prs': [data['pr_count'] for data in monthly_data],
            'all_time_max': float(ExerciseHistory.objects.filter(
                user=request.user,
                exercise_name=exercise,
                personal_record=True
            ).aggregate(Max('weight'))['weight__max'] or 0)
        }

    context = {
        'progress_data': json.dumps(progress_data, cls=DecimalEncoder),
        'exercises': exercises
    }
    return render(request, 'progress.html', context)

def about(request):
    return render(request, "about.html")

def coach(request):
    return render(request, "coach.html")

def generate_reset_code():
    return ''.join(random.choices(string.digits, k=6))

def password_reset(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'request_code':
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                reset_code = generate_reset_code()
                
                # Store code in session with 10-minute expiration
                request.session['reset_code'] = reset_code
                request.session['reset_email'] = email
                request.session['code_expiry'] = (timezone.now() + timedelta(minutes=10)).timestamp()
                
                messages.success(request, f'Reset code has been generated: {reset_code}')
                return render(request, 'ResetPassword.html', {'show_code_input': True})
                
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
        
        elif action == 'reset_password':
            stored_code = request.session.get('reset_code')
            stored_email = request.session.get('reset_email')
            expiry_time = request.session.get('code_expiry')
            
            if not all([stored_code, stored_email, expiry_time]):
                messages.error(request, 'Reset session expired. Please try again.')
                return redirect('password_reset')
            
            if timezone.now().timestamp() > expiry_time:
                messages.error(request, 'Reset code expired. Please request a new one.')
                return redirect('password_reset')
            
            entered_code = request.POST.get('code')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if entered_code != stored_code:
                messages.error(request, 'Invalid reset code.')
                return render(request, 'ResetPassword.html', {'show_code_input': True})
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'ResetPassword.html', {'show_code_input': True})
            
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'ResetPassword.html', {'show_code_input': True})
            
            try:
                user = User.objects.get(email=stored_email)
                user.password = make_password(new_password)
                user.save()
                
                # Clear session data
                for key in ['reset_code', 'reset_email', 'code_expiry']:
                    if key in request.session:
                        del request.session[key]
                
                messages.success(request, 'Password has been reset successfully.')
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, 'Error resetting password. Please try again.')
    
    return render(request, 'ResetPassword.html', {'show_code_input': False})