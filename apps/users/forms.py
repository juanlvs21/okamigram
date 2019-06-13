"""User forms."""
# Django
from django import forms

# Models 
from django.contrib.auth.models import User
from apps.users.models import Profile

class SignupForm(forms.Form):
    """Sign up form."""
    username = forms.CharField(min_length=4, max_length=50)
    
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())

    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())
    
    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        query = User.objects.filter(username=username).exists()

        if query:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data
    
    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data) # **data sirve para enviar todos los atributos del diccionario
        profile = Profile(user=user,picture="users/pictures/perfil.png")
        profile.save()

class PictureForm(forms.Form):
    """Pircture form."""
    picture = forms.ImageField(required=True)
