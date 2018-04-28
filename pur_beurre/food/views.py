"""All the views for the food app of the pur_beurre project"""


# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import Http404

# Imports from my app
from .models import NutritionGrade, Category, Food, MySelection
from .forms import AccountForm, ParagraphErrorList, ConnexionForm



####### PAGE D'ACCUEIL #######
def home(request):
    """View to the homepage."""
    return render(request, 'food/home.html')


####### CREATION DE COMPTE #######
def register(request):
    """View to the user account creation page and validation of the user form."""
    if request.method == "POST":
        form = AccountForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            form.save()    ######
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticated(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            context['errors'] = form.errors.items()
    else:
        form = AccountForm()
    context = {'form': form}
    return render(request, 'food/register.html', context)


####### MON COMPTE #######
@login_required(login_url='/account/register/', redirect_field_name='redirection_vers')
def account(request):
    """View to the user account information page."""
    return render(request, 'food/account.html')

####### CONNEXION #######
def signin(request):
    """View to the log in page."""
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
    return render(request, 'food/signin.html', context)


####### DECONNEXION #######
def signout(request):
    """Log out function."""
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
    selection_list = Food.objects.filter(
        nutrition_grade__lt=food.nutrition_grade)
    selection_list = selection_list.order_by(
        'nutrition_grade', 'nutrition_score', 'name', 'brand')
    selection_list = selection_list.distinct('name')[:6]
    return render(request, 'food/foodresult.html')


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
