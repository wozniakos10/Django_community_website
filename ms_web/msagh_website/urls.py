from django.urls import path
from . import views

app_name = "msagh_website"

urlpatterns = [
    path('',views.base,name='base'),
    path('spotted/', views.spotted, name='spotted'),
    path('new_spot', views.new_spot, name="new_spot"),
    path('memes/', views.memes, name="memes"),
]