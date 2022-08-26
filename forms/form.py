from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class RegistrationFrom(UserCreationForm):
    first_name = forms.CharField(max_length=30 ,  required=True)
    email = forms.EmailField(max_length=30 ,  required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

        def clean_email(self):
            print("email cleaning")
            email= self.cleaned_data['email']
            User = None

            try:
                user = User.objects.get(email=email)
            except:
                return email

            if(email is not None):
                raise ValidationError("email already there")
