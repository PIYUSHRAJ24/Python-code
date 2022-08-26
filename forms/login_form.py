from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django import forms
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=30, required = True , label = 'EmailAdress')


    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user =None

        try:
            user = User.objects.get(email = email)
            result = authenticate(username = user.username , 
            password = password)
            print ("result is show" , result)

            if result is not None:
                # login(self.request, result)
                return result
            else:
                raise forms.ValidationError("Email or password Wrong")
        except:
            raise forms.ValidationError("Email or password Wrong")
