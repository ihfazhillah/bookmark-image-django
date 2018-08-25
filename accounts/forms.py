from django import forms
from django.contrib.auth.models import User
from .models import Profile

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)

        for field_name in iter(self.fields):
           field = self.fields[field_name]
           classes = field.widget.attrs.get('class')

           if classes:
               classes += ' form-control pb-3'
           else:
               classes = 'form-control pb-3'

           field.widget.attrs.update({'class': classes})


class UserEditForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(BootstrapModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(BootstrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='Repeat Password')


    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')


    def clean_password2(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Password didn\'t match')
        return cleaned_data['password2']
