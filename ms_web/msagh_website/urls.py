from django.urls import path
from . import views

app_name = "msagh_website"

urlpatterns = [
    path('',views.base,name='base_html'),
]