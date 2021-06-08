from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.home_view),
    path('about/', views.about_view),
    path('auth/login/', views.UserLoginView.as_view()),
    path('admin/', admin.site.urls),
]
