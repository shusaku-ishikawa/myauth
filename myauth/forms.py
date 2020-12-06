from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm
)
from django import forms
from .models import (
    User,
)

form_input_base_class = 'p-2 form-input block border w-full mb-5 '
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': form_input_base_class,
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': form_input_base_class,
            }
    )
)

class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    class Meta:
        model = User
        fields = [
            'family_name', 
            'first_name', 
            'zip',
            'address',
            'phone',
            'unnamed1',
            'unnamed2',
            'unnamed3',
            'unnamed4',
            'password1', 
            'password2', 
        ]
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = form_input_base_class

    def get_next_id(self):
        usercount = User.objects.all().count()
        return str(1000 + usercount)

    # @override
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_id = self.get_next_id()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = User
        fields = (
            'zip',
            'address',
            'phone',
            'unnamed1',
            'unnamed2',
            'unnamed3',
            'unnamed4',
        )
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.required:
                visible.field.label = f'{visible.field.label}*'
            visible.field.widget.attrs['class'] = form_input_base_class

class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = form_input_base_class