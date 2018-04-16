"""All the views for the food app of the pur_beurre project"""


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import MyAccount, Category, Food, MyHealthyFood
from .models import NutritionGrade

from .forms import AccountForm, ParagraphErrorList, ConnexionForm



def home(request):
    """View to the homepage"""
    return render(request, 'food/home.html')

def account(request):
    """View to the user account page"""
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
    """View to the log in page"""
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

# def deconnexion(request):
#     """Log out function"""
#     logout(request)
#     return redirect(reverse(connexion))

def foodresult(request):
    """View to the page that displays all the food products
    related to the category searched by the user"""
    # query = request.GET.get('query')
    # Query = get_object_or_404(Food)
    # if not query:
    return render(request, 'food/foodresult.html')

def foodinfo(request):
    """View to the page that gives food information for each product"""
    return render(request, 'food/foodinfo.html')

def selection(request):
    """View to the user's personal selection of healthy food"""
    return render(request, 'food/selection.html')

def credits(request):
    """View to the page for photos, icons, images, etc., credits"""
    return render(request, 'food/credits.html')
