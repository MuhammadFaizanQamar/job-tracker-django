from django.core.paginator import Paginator
from .models import JobApplication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import JobApplicationSerializer

@login_required(login_url='login')
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    
    status = request.GET.get('status', '')
    if status:
        jobs = jobs.filter(status=status)
    
    search = request.GET.get('search', '')

    if search:
        jobs = jobs.filter(company__icontains=search)

    
        # -------------------------
    # PAGINATION ADDED HERE
    # -------------------------
    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,  # IMPORTANT: replace jobs with page_obj
        'page_obj': page_obj,

        'total': jobs.count(),
        'applied': JobApplication.objects.filter(user=request.user, status='applied').count(),
        'interview': JobApplication.objects.filter(user=request.user, status='interview').count(),
        'offer': JobApplication.objects.filter(user=request.user, status='offer').count(),
        'rejected': JobApplication.objects.filter(user=request.user, status='rejected').count(),

        'selected_status': status,
        'search': search,
    }
    return render(request, 'jobs/dashboard.html', context)

@login_required(login_url='login')
def jobdetail(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    
    context = {
            'job': job,
    }
    return render(request, 'jobs/job_detail.html', context)

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'jobs/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


class JobListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = JobApplication.objects.filter(user=request.user)
        serializer = JobApplicationSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class JobDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, job_id, user):
        return get_object_or_404(JobApplication, id=job_id, user=user)

    def get(self, request, job_id):
        job = self.get_object(job_id, request.user)
        serializer = JobApplicationSerializer(job)
        return Response(serializer.data)

    def put(self, request, job_id):
        job = self.get_object(job_id, request.user)
        serializer = JobApplicationSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        job = self.get_object(job_id, request.user)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)