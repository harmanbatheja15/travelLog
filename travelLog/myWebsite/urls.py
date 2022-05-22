from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('travelLogs/', views.travelLogs, name='travelLogs'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addLog/', views.addLog, name='addLog'),
    path('editLog/<int:log_id>', views.editLog, name='editLog'),
    path('travelLogs/<int:log_id>/uploadImages', views.uploadImages, name='uploadImages'),
    path('travelLogs/detail/<int:log_id>/', views.detail, name='detail'),
]
