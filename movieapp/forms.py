from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class RegistrationForm(UserCreationForm):
     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True)
     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label="Password")
     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label="Confirm Password")

     class Meta:
          model=User
          fields = ['username','email','password1','password2']


class CustomerProfileForm(forms.ModelForm):
     class Meta:
          model = Customer
          fields = ['name','city','mobile','state','zipcode']
          widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'zipcode': forms.TextInput(attrs={'class':'form-control'}),
          }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}))



class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email', 
            'aria-label': 'Email address'
        }),
        required=True
    )
