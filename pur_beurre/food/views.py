"""All the views for the food app of the pur_beurre project"""


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import MySelection, Category, Food
from .models import NutritionGrade

from .forms import AccountForm, ParagraphErrorList, ConnexionForm



def home(request):
    """View to the homepage"""
    return render(request, 'food/home.html')

def register(request):
    """View to the user account creation page"""
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
    return render(request, 'food/register.html', context)

def account(request):
    """View to the user account page"""
    return render(request, 'food/account.html')

def login(request):
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
    return render(request, 'food/login.html', context)

def logout(request):
    """Log out function"""
    logout(request)
    return redirect(reverse(login))

def foodresult(request):
    """View to the page that displays all the food products
    related to the category searched by the user"""
    # query = request.GET.get('text')
    # list_query = query.split(',')
    # textname = list_query[0]
    # textbrand = list_query[1]    
    # food_search = Food.objects.filter(
    #     name__icontains = textname,
    #     brand__icontains = textbrand)[0]
    # category_search = food_search.category.all()
    selection_list = Food.objects.filter(
        nutrition_grade__lt = food.nutrition_grade)
    selection_list = selection_list.order_by(
        'nutrition_grade', 'nutrition_score', 'name', 'brand')
    selection_list = selection_list.distinct('name')[:6] 
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
