from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .signals import user_logged_in


class UserLoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'auth/login.html'

    def form_valid(self, form):
        request = self.request

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
        return super(UserLoginView, self).form_valid(form)


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required
def about_view(request):
    return render(request, 'about.html')
