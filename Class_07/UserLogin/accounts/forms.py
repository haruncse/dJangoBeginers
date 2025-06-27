from django import forms
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")