from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account, Log, LogImage

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=100, help_text="Required, Enter a valid email address!")

    class Meta:
        model = Account
        fields = ("name", "phone", "email", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")

class DateInput(forms.DateInput):
    input_type = 'date'

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('title', 'location', 'date', 'image', 'description', 'visibility')
        widgets = {
            'title': forms.TextInput(attrs={'required': 'true', 'autocomplete': 'off'}),
            'location': forms.TextInput(attrs={'required': 'true', 'autocomplete': 'off'}),
            'date': DateInput(),
            'image': forms.FileInput(),
            'visibility': forms.Select(attrs={'required': 'true'})
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = LogImage
        fields = ('image', )
