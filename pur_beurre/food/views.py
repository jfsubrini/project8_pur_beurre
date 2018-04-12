from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
# from django.core.urlresolvers import reverse
from django.urls import reverse

# from .models import MyAccount, Category, Food, MyHealthyFood
# from .models import NutritionGrade

from .forms import AccountForm, ParagraphErrorList, ConnexionForm



def home(request):
    return render(request, 'food/home.html')

def account(request):
    if request.method == "POST":
        form = AccountForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            context = {'username' : username, 'email' : email, 'password' : password}
            return render(request, 'food/account.html', context)
        else:
            context['errors'] = form.errors.items()
    else:
        form = AccountForm()
    context = {'form': form}
    return render(request, 'food/account.html', context)

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True
    else:
        form = ConnexionForm()
    context = {'form': form}
    return render(request, 'food/connexion.html', context)

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))

def credits(request):
    return render(request, 'food/credits.html')

def selection(request):
    return render(request, 'food/selection.html')
