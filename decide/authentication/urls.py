from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

from .views import GetUserViewAPI, LogoutViewAPI, RegisterViewAPI, RegisterView, LoginView, SuccessView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutViewAPI.as_view()),
    path('getuser/', GetUserViewAPI.as_view()),
    path('register/', RegisterViewAPI.as_view()),
    path('register-alt/', RegisterView.as_view()),
    path('login-alt/', LoginView.as_view(),name="login"),
    path("logout-alt/", auth_views.LogoutView.as_view(), name="logout"),
    path('login-success/', SuccessView.as_view(),name="login-success")
]
