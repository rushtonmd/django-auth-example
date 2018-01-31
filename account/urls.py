from django.urls import path
from .views import AccountViewFactory, PasswordResetViewFactory

# TODOs Here are all the auth views that need to be created
# https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views
# Code: https://github.com/django/django/blob/master/django/contrib/auth/views.py


urlpatterns = [
    path('signup/', AccountViewFactory.create_view('signup'), name='signup'),
    path('signup/needs-activation', AccountViewFactory.create_view('needs_activation'), name='needs_activation'),
    path('signup/activation-successful', AccountViewFactory.create_view('activation_successful'), name='activation_successful'),
    path('signup/activation-invalid', AccountViewFactory.create_view('activation_invalid'), name='activation_invalid'),
    path('login/', AccountViewFactory.create_view('login'), name='login'),
    path('logout/', AccountViewFactory.create_view('logout'), name='logout'),
    path('activate/<uidb64>/<token>/', AccountViewFactory.create_view('activate'), name='activate'),
    path('password-reset/', PasswordResetViewFactory.create_password_form_view(), name='password_reset'),
    path('password-reset/done', PasswordResetViewFactory.create_password_reset_done_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetViewFactory.create_password_reset_confirm_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetViewFactory.create_password_reset_complete_view(), name='password_reset_complete'),
    path('password-change/', AccountViewFactory.create_view('password_change'), name='password_change'),
    path('password-change/done', AccountViewFactory.create_view('password_change_done'), name='password_change_done'),
]
