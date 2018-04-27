"""Forms to create the user account and for the log in"""


from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
# from django import forms
from django.forms.utils import ErrorList

from django.contrib.auth.models import User



class AccountForm(ModelForm):
    """Form to create the user account, based on the Account model"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputEmail', 'placeholder': 'Entrez votre email'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }


class ParagraphErrorList(ErrorList):
    """Function to manage the validation errors in the forms"""
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' \
            % e for e in self]) #### A revoir 34 et 35


class ConnexionForm(ModelForm):
    """Form for the log in, based on the Account model"""
    
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', \
                'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }
