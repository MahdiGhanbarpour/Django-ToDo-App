from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm

# Create your views here.
class CustomLoginView(LoginView):
    '''
    A custom view to login user
    '''
    template_name = "accounts/login.html"
    fields = ["username", "password"]
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:task-list")
    
class CustomRegisterView(FormView):
    '''
    A custom view to register user with custom registration form
    '''
    template_name = "accounts/register.html"
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:task-list")
        return super(CustomRegisterView, self).get(*args, **kwargs)