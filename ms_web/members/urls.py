from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('',views.register,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('profile/<int:pk>',views.profile, name='profile'),
]