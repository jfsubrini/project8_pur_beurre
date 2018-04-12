""" Form to register the user account """

from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.forms.utils import ErrorList

from .models import MyAccount



class AccountForm(ModelForm):
    class Meta:
        model = MyAccount
        fields = '__all__'
        widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', 'id': 'inputEmail', 'placeholder': 'Entrez votre email'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class ConnexionForm(ModelForm):
    class Meta:
      model = MyAccount
      exclude = ('email',)
      widgets = {
            'username': TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'username', 'placeholder': 'Entrez votre nom d\'utilisateur'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'inputPassword', 'placeholder': 'Entrez votre mot de passe'})
        }
