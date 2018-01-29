from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomLoginForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)


class SignupViewOld(View):
    def post(self, request):
        # form = EmailPostForm(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     send_mail('Sample Message', 'comment', 'test@test.com', list('mark@rushtonmd.com'))
        return redirect('/admin')

    def get(self, request):
        form = UserCreationForm()

        return render(request, 'account/signup.html', {'form': form})


class SignupView(auth_views.PasswordContextMixin, FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('/')
    template_name = 'account/signup.html'
    title = _('Signup')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


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
