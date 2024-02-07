from typing import Any
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponse as HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from users.models import Person, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, ProfileUserForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from .mixins import BtnTitleMixin



# Create your views here.
class IndexView(ListView):
    template_name = 'index.html'
    model = Person
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['current_user'] = self.request.user
        context['current_user_id'] = self.request.user.id
        
        context['users'] = Person.objects.all().order_by('username')
        return context

class DetailUserView(DetailView):
    model = Person
    template_name = 'user_detail.html'
    
    def get_object(self, queryset=None):
        return Person.objects.get(id=self.kwargs.get("id"))

class ProfileUserView(UpdateView):
    model = Person
    template_name = 'user_edit.html'
    form_class = ProfileUserForm
    success_url = reverse_lazy('users:index')
    # btn_title = 
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['btn_title'] = "Изменить пользователя"
        return context
    
    def get_object(self, queryset=None):
        
        return Person.objects.get(id=self.kwargs.get("id"))
    
    

class DeleteUserView(BtnTitleMixin, DeleteView):
    model = Person
    template_name = 'user_delete.html'
    btn_title = "Удалить пользователя"
    
    def get_object(self, queryset=None):
        return Person.objects.get(id=self.kwargs.get("id"))
    
    success_url = reverse_lazy('users:index')

class LoginUserView(BtnTitleMixin, LoginView):
    model = Person
    template_name = 'user_login.html'
    form_class = UserLoginForm
    btn_title = "Войти"
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse_lazy('users:index')


class LogoutUserView(LogoutView):
    model = Person
    http_method_names = ['get']
    
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request=request)
        return redirect('users:index')
    

class RegistrationUserView(BtnTitleMixin, CreateView):
    model = Person
    template_name = 'user_register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    btn_title = "Зарегистрироваться"
    
    
class UserPasswordChangeView(BtnTitleMixin, PasswordChangeView):
    model = Person
    template_name = 'user_password_change.html'
    success_url = reverse_lazy("users:password_change_done")
    btn_title = "Изменить пароль"
    
    
class UserPasswordResetView(BtnTitleMixin, PasswordResetView):
    model = Person
    template_name = 'user_password_reset.html'
    success_url = reverse_lazy("users:login")
    btn_title = "Сбросить пароль"
    
    
class UserPasswordChangeDoneView(PasswordResetDoneView):
    model = Person
    template_name = 'password_reset_done.html'
    
class EmailVerificationView(TemplateView):
    template_name = "email_verification.html"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        code = kwargs['code']
        user = Person.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification and email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:index'))