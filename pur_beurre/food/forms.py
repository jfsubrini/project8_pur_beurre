""" Form to register the user account """

from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.forms.utils import ErrorList

from .models import MyAccount


# class AccountForm(forms.Form):
#     username = forms.CharField(max_length=100, label="Votre nom : ")
#     email = forms.EmailField(max_length=100, label="Votre email : ")
#     password = forms.CharField(max_length=100,
#       widget=forms.PasswordInput, label="Votre mot de passe : ")


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


### Pour le Sign In, mais attention car name est obligatoire, pas null
# class AccountForm(forms.ModelForm):
#     class Meta:
#       model = MyAccount
#       exclude = ('name')


class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=30, label="Votre nom : ")
    password = forms.CharField(max_length=100,
        widget=forms.PasswordInput, label="Votre mot de passe : ")
