"""Forms to create the user account and for the sign in."""


# Django imports
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.forms.utils import ErrorList

from django.contrib.auth.models import User




class AccountForm(ModelForm):
    """Form to create the user register account, based on the Django User model."""

    class Meta:
        """Details of the register form and attributes settings for CSS."""
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputEmail', 'placeholder': 'Entrez votre email', 'required': 'required'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }


class ValidationErrorList(ErrorList):
    """Function to manage the validation errors in the forms."""
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return ''.join([e for e in self])


class ConnexionForm(ModelForm):
    """Form for the sign in, based on the Django User model."""

    class Meta:
        """Details of the sign in form and attributes settings for CSS."""
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }
