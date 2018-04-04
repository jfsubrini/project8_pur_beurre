from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'title': 'Mon super titre'}
    return render(request, 'resultats/index.html', context)

def food(request):
    #
    return render(request, 'resultats/food.html', context)

def index(request):
    #
    return render(request, 'resultats/index.html', context)