from django.shortcuts import render
from .models import JobApplication


def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    context = {
        'jobs': jobs
    }
    return render(request, 'jobs/dashboard.html', context)