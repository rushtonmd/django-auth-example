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


class SignupView(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account... please.'
            message = render_to_string('account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # send_mail('DJANGO TEST MESSAGE', 'Here is the body.', 'test@test.com', [to_email])
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


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = CustomLoginForm()
    return render(request, 'account/login.html', {'form': form})
