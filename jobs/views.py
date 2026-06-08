from .models import JobApplication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required(login_url='login')
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    context = {
        'jobs': jobs
    }
    return render(request, 'jobs/dashboard.html', context)

@login_required(login_url='login')
def add_job(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # saves to memory, not database yet
            job.user = request.user        # attach the logged in user
            job.save() 
            return redirect('dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/addjob.html', {'form': form})

@login_required(login_url='login')
def delete_job (request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    job.delete()
    return redirect('dashboard')

@login_required(login_url='login')
def edit_job(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JobApplicationForm(instance=job)
    
    return render(request, 'jobs/editjob.html', {'form': form})   

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'jobs/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')