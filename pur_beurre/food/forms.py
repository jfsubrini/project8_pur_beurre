from django import forms



class AccountForm(forms.Form):
    name = forms.CharField(max_length=100, label="Votre nom : ")
    email = forms.EmailField(max_length=100, label="Votre email : ")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label="Votre mot de passe : ") ### Champ spécial password existe ?
