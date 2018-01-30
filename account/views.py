from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

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


class AccountViewFactory():
    # Define a method to create a SignupView
    # The method needs to return a CLASS.as_view(), as you can't
    # call .as_view() on an instance
    #
    def create_signup_view():
        signupView = SignupView

        # Override the attribute for EmailGenerator
        signupView.EmailGenerator = EmailMessage

        # Override the class attribute for SignupForm
        signupView.SignupForm = CustomUserCreationForm

        # Return the view using the as_view() method
        return signupView.as_view()


class PasswordResetViewFactory():
    def create_password_form_view():
        view = auth_views.PasswordResetView

        view.template_name = 'password_reset/password_reset_form.html'
        view.email_template_name = 'password_reset/password_reset_email.html'
        view.subject_template_name = 'password_reset/password_reset_subject.txt'

        return view.as_view()

    def create_password_reset_done_view():
        view = auth_views.PasswordResetDoneView

        view.template_name = 'account/generic_message.html'
        message = render_to_string('password_reset/password_reset_done.html')
        view.extra_context = {'message': message}

        return view.as_view()

    def create_password_reset_complete_view():
        view = auth_views.PasswordResetCompleteView

        view.template_name = 'account/generic_message.html'
        message = render_to_string('password_reset/password_reset_complete.html')
        view.extra_context = {'message': message}

        return view.as_view()

    def create_password_reset_confirm_view():
        view = auth_views.PasswordResetConfirmView

        view.template_name = 'password_reset/password_reset_confirm.html'

        return view.as_view()


class SignupView(View):
    EmailGenerator = EmailMessage
    SignupForm = CustomUserCreationForm

    def send_email(self, request, user, form):
        email_generator = SignupView.EmailGenerator
        mail_subject = 'Activate your account... please.'
        current_site = get_current_site(request)
        message = render_to_string('account/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('username')
        email = email_generator(mail_subject, message, to=[to_email])
        email.send()

    def post(self, request):
        form = SignupView.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            self.send_email(request, user, form)
            return redirect('needs_activation')
        else:
            return render(request, 'account/signup.html', {'form': form})

    def get(self, request):
        form = CustomUserCreationForm()

        return render(request, 'account/signup.html', {'form': form})


class CustomLoginView(auth_views.LoginView):
    """
    Custom login view.
    """

    form_class = CustomLoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):

        return super(CustomLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        return super(CustomLoginView, self).form_valid(form)


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user)
            # return redirect('home')
            return redirect('activation_successful')
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return redirect('activation_invalid')
            # return HttpResponse('Activation link is invalid!')


class NeedsActivationView(TemplateView):
    template_name = 'account/generic_message.html'

    def get(self, request):
        return render(request, self.template_name, {'message': "Please check your email to active your account."})


class AccountActivatedView(TemplateView):
    template_name = 'account/generic_message.html'

    def get(self, request):
        return render(request, self.template_name, {'message': "Your account has been successfully activated!"})


class InvalidActivationView(TemplateView):
    template_name = 'account/generic_message.html'

    def get(self, request):
        return render(request, self.template_name, {'message': "Invalid activation link."})


class CustomLogoutView(auth_views.LogoutView):
    template_name = 'account/generic_message.html'

    def get(self, request):
        return render(request, self.template_name, {'message': "You have been logged out!"})
