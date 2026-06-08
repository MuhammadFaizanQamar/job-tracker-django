from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_job, name='add_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobdetail/<int:job_id>/', views.jobdetail, name='jobdetail'),

    path('api/jobs/', views.JobListAPI.as_view(), name='api_jobs'),
    path('api/jobs/<int:job_id>/', views.JobDetailAPI.as_view(), name='api_job_detail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]