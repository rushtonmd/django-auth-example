from django.shortcuts import render
from django.views import View
from django.contrib.auth import views as auth_views

from .forms import CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AccountViewFactory():
    account_types = (
        'signup',
        'needs_activation',
        'activation_successful',
        'activation_invalid',
        'logout',
        'login',
        'activate',
        'password_change',
        'password_change_done',
        'password_reset',
        'password_reset_done',
        'password_reset_confirm',
        'password_reset_complete',
        )

    @classmethod
    def create_signup(cls, **kwargs):
        # Get the SignupView class
        view = SignupView

        # Return the updated SignupView as a view
        return view.as_view(**kwargs)

    @classmethod
    def create_needs_activation(cls, **kwargs):
        # Get the GenericMessageView class
        view = GenericMessageView

        # Set the default message
        default_message = {'message': 'Please check your email to active your account.'}

        # Combine the keyword arguments
        combined_args = {**default_message, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_activation_successful(cls, **kwargs):
        # Get the GenericMessageView class
        view = GenericMessageView

        # Set the default message
        default_message = {'message': 'Your account has been successfully activated!'}

        # Combine the keyword arguments
        combined_args = {**default_message, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_activation_invalid(cls, **kwargs):
        # Get the GenericMessageView class
        view = GenericMessageView

        # Set the default message
        default_message = {'message': 'Invalid activation link.'}

        # Combine the keyword arguments
        combined_args = {**default_message, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_logout(cls, **kwargs):
        # Get the GenericMessageView class
        view = CustomLogoutView

        # Set the default args
        default_args = {
            'message': 'You have been successfully logged out.',
            'next_page': reverse_lazy('login'),
            }

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_login(cls, **kwargs):
        # Get the GenericMessageView class
        view = auth_views.LoginView

        # Set the default args
        default_args = {'template_name': 'account/login.html'}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_activate(cls, **kwargs):
        # Get the ActivateUser class
        view = ActivateUser

        # Return the updated view with the combined args
        return view.as_view(**kwargs)

    @classmethod
    def create_password_change(cls, **kwargs):
        # Get the ActivateUser class
        view = auth_views.PasswordChangeView

        # Set the default args
        default_args = {'template_name': 'password_reset/password_change_form.html'}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_password_change_done(cls, **kwargs):
        # Get the ActivateUser class
        view = GenericMessageView

        # Set the default message
        default_message = {'message': 'Password Change Complete!'}

        # Combine the keyword arguments
        combined_args = {**default_message, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_password_reset(cls, **kwargs):
        # Get the ActivateUser class
        view = auth_views.PasswordResetView

        # Set the default message
        default_args = {
            'template_name': 'password_reset/password_reset_form.html',
            'email_template_name': 'password_reset/password_reset_email.html',
            'subject_template_name': 'password_reset/password_reset_subject.txt'}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_password_reset_done(cls, **kwargs):
        # Get the ActivateUser class
        view = auth_views.PasswordResetDoneView

        # Create the message
        message = render_to_string('password_reset/password_reset_done.html')

        # Set the default message
        default_args = {
            'template_name': 'account/generic_message.html',
            'extra_context': {'message': message}}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_password_reset_confirm(cls, **kwargs):
        # Get the ActivateUser class
        view = auth_views.PasswordResetConfirmView

        # Set the default message
        default_args = {'template_name': 'password_reset/password_reset_confirm.html'}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_password_reset_complete(cls, **kwargs):
        # Get the ActivateUser class
        view = auth_views.PasswordResetCompleteView

        # Create the message
        message = render_to_string('password_reset/password_reset_complete.html')

        # Set the default message
        default_args = {
            'template_name': 'account/generic_message.html',
            'extra_context': {'message': message}}

        # Combine the keyword arguments
        combined_args = {**default_args, **kwargs}

        # Return the updated view with the combined args
        return view.as_view(**combined_args)

    @classmethod
    def create_view(cls, type, **kwargs):
        if type not in cls.account_types:
            return None

        return getattr(cls, 'create_' + type)(**kwargs)


class SignupView(View):
    email_generator = EmailMessage
    signup_form = CustomUserCreationForm
    needs_activation_template = 'needs_activation'
    template_name = 'account/signup.html'
    email_template_name = 'account/signup_email.html'
    subject_template_name = 'account/signup_email_subject.txt'

    def send_email(self, request, user, form):
        mail_subject = render_to_string(self.subject_template_name).strip('\n')
        current_site = get_current_site(request)
        message = render_to_string(self.email_template_name, {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('username')
        email = self.email_generator(mail_subject, message, to=[to_email])
        email.send()

    def post(self, request):
        form = self.signup_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            self.send_email(request, user, form)
            return redirect(self.needs_activation_template)
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = self.signup_form()

        return render(request, self.template_name, {'form': form})


class ActivateUser(View):
    # Set the initial value for the redirect path on a succesful activation
    redirect_success = 'activation_successful'

    # Set the initial value for the redirect path on an invalid activation
    redirect_invalid = 'activation_invalid'

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(self.redirect_success)
        else:
            return redirect(self.redirect_invalid)


class GenericMessageView(TemplateView):
    template_name = 'account/generic_message.html'
    message = ''

    def get(self, request):
        return render(request, self.template_name, {'message': self.message})


class CustomLogoutView(auth_views.LogoutView):
    template_name = 'account/generic_message.html'
    message = ''

    def get(self, request):
        return render(request, self.template_name, {'message': self.message})
