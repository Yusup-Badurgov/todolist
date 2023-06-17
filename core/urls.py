from django.urls import path
from core.views import UserRegistrationView, LoginViews, UserProfileView, ChangePasswordView

urlpatterns = [
    path('login', LoginViews.as_view(), name='login'),
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
    path('update_password', ChangePasswordView.as_view(), name='user-profile'),

]