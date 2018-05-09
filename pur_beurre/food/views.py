"""All the views for the food app of the pur_beurre project."""


# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

# Imports from my app
from .models import NutritionGrade, Category, Food, MySelection
from .forms import AccountForm, ValidationErrorList, ConnexionForm



####### PAGE D'ACCUEIL #######
def home(request):
    """View to the homepage."""
    return render(request, 'food/home.html')


####### CREATION DE COMPTE #######
def register(request):
    """View to the user account creation page and validation of the user form."""
    # Analysis and treatment of the register form that has been sent.
    if request.method == "POST":
        form = AccountForm(request.POST, error_class=ValidationErrorList)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, email=email, password=password)
            # If data are valid, automatic log in and redirection to 'Mon Compte' page.
            login(request, user)
            return redirect('account')
    else:
        form = AccountForm()

    context = {
        'form': form,
        'errors': form.errors.items()
        }
    return render(request, 'food/register.html', context)


####### MON COMPTE #######
@login_required(login_url='/account/register/', redirect_field_name='redirection_vers')
def account(request):
    """View to the user account information page."""
    return render(request, 'food/account.html')


####### CONNEXION #######
def signin(request):
    """View to the log in page."""
    signin_failed = False

    # In case the user is already logged in, redirection to homepage.
    if request.user.is_authenticated:
        return redirect('home')

    # Analysis and treatment of the sign in form that has been sent.
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # If the connexion is valid, log in and redirection to 'Mon Compte' page.
            if user is not None:
                login(request, user)
                return redirect('account')
            else:
                signin_failed = True
    else:
        form = ConnexionForm()

    context = {
        'form': form,
        'errors': form.errors.items(),
        'signin_failed': signin_failed
        }
    return render(request, 'food/signin.html', context)


####### DECONNEXION #######
def signout(request):
    """Log out function with redirection to homepage."""
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


####### RESULTATS DE LA RECHERCHE #######
def foodresult(request):
    """View to the page that displays all the food products
    related to the category searched by the user."""
    # query = request.GET.get('text')
    # list_query = query.split(',')
    # textname = list_query[0]
    # textbrand = list_query[1]
    # food_search = Food.objects.filter(
    #     name__icontains=textname,
    #     brand__icontains=textbrand)[0]
    # category_search = food_search.category.all()
    food_list = Food.objects.filter(
        nutrition_grade__lt=food.nutrition_grade)
    food_list = food_list.order_by(
        'nutrition_grade', 'nutrition_score', 'name', 'brand')
    food_list = food_list.distinct('name')
    paginator = Paginator(food_list, 6)
    page = request.GET.get('page')
    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)
    context = {
        'foods': foods,
        'paginate': True
    }
    return render(request, 'food/foodresult.html', context)


####### PAGE D'INFORMATION SUR L'ALIMENT #######
def foodinfo(request):
    """View to the page that gives food information for each product."""
    return render(request, 'food/foodinfo.html')


####### PAGE DE SELECTION DES ALIMENTS SAINS #######
def selection(request):
    """View to the user's personal selection of healthy food."""
    return render(request, 'food/selection.html')


####### MENTIONS LEGALES #######
def credits(request):
    """View to the page for photos, icons, images, etc., credits."""
    return render(request, 'food/credits.html')
