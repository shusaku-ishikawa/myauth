from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from django.views.generic import (
    CreateView, UpdateView, TemplateView, ListView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import (
    LoginForm, ProfileForm, SignUpForm, PasswordForm
)
from .models import (
    User,
)

class OnlySuperuserMixin(UserPassesTestMixin):
    raise_exception = False # set True if raise 403_Forbidden

    def test_func(self):
        user = self.request.user
        return user.is_superuser

class OnlyYouOrSuperuserMixin(UserPassesTestMixin):
    raise_exception = False # set True if raise 403_Forbidden

    def test_func(self):
        user = self.request.user
        if 'pk' in self.kwargs:
            return user.pk == self.kwargs['pk'] or user.is_superuser
        else:
            return user.is_superuser

# Create your views here.
class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'myauth/login.html'

class Logout(LogoutView):
  pass

class Top(LoginRequiredMixin, TemplateView):
    template_name = 'myauth/top.html'

class Profile(OnlyYouOrSuperuserMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'myauth/profile.html'
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['user'] = self.request.user
        return ret

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        ret = super().form_valid(form, **kwargs)
        messages.success(self.request, '更新しました。')
        return ret

    def get_success_url(self):
        return reverse_lazy('myauth:profile', kwargs={ 'pk': self.kwargs['pk'] })
    
class SignUp(OnlySuperuserMixin, CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('myauth:login')
    template_name = 'myauth/signup.html'
    

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.success(self.request, f'ユーザ:{self.object.user_id} 登録完了しました。')
        return ret

class ChangePassword(OnlyYouOrSuperuserMixin, PasswordChangeView):
    template_name = 'myauth/change_password.html'
    form_class = PasswordForm
    
    def get_success_url(self):
        messages.success(self.request, 'パスワードを更新しました')
        return reverse_lazy('myauth:profile', kwargs = { 'pk': self.request.user.pk })    
    
class ListUser(OnlySuperuserMixin, ListView):
    model = User
    template_name = 'myauth/list_user.html'
    queryset = User.objects.all().order_by('pk')

class DeleteUser(OnlySuperuserMixin, DeleteView):
    model = User
    template_name = 'myauth/delete_user.html'
    success_url = reverse_lazy('myauth:list_user')
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['user'] = self.request.user
        return ret
