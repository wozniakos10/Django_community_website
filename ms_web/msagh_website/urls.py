from django.urls import path
from. import views
from django.contrib.auth import views as auth_views #import this

app_name = "msagh_website"

urlpatterns = [
    path('',views.base,name='base'),
    path('spotted/<int:pk>', views.one_spot, name="one_spot"),
    path('spotted/', views.spotted, name='spotted'),
    path('new_spot', views.new_spot, name="new_spot"),
    # path('memes/', views.memes, name="memes"),
    # path('memes/<int:pk>', views.one_meme, name="one_meme"),
    # path('new_meme/',views.new_meme,name='new_meme'),
    path('contact/', views.contact, name="contact"),
    path("password_reset/", views.password_reset_request, name="password_reset"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    # URL connected with passsword
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
        name='password_reset_complete'),

]