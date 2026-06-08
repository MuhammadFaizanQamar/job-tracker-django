from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_job, name='add_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
]