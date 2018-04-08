from django.shortcuts import render


def home(request):
    context = {'title': 'Mon super titre'}
    return render(request, 'food/home.html', context)
