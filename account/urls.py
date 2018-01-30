from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .views import AccountViewFactory, PasswordResetViewFactory
from django.urls import reverse_lazy

# TODOs Here are all the auth views that need to be created
# https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views
# Code: https://github.com/django/django/blob/master/django/contrib/auth/views.py
#
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']

urlpatterns = [
    # path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/', AccountViewFactory.create_signup_view(), name='signup'),
    path('signup/needs-activation', views.NeedsActivationView.as_view(), name='needs_activation'),
    path('signup/activation-successful', views.AccountActivatedView.as_view(), name='activation_successful'),
    path('signup/activation-invalid', views.InvalidActivationView.as_view(), name='activation_invalid'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateUser.as_view(), name='activate'),
    path('password-reset/', PasswordResetViewFactory.create_password_form_view(), name='password_reset'),
    path('password-reset/done', PasswordResetViewFactory.create_password_reset_done_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetViewFactory.create_password_reset_confirm_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetViewFactory.create_password_reset_complete_view(), name='password_reset_complete'),

    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

]
