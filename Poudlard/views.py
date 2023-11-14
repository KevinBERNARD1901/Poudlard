from .models import Character
from django.shortcuts import render, get_object_or_404


# Create your views here.

def character_list(request):
    characters = Character.objects.all()
    return render(request, 'Poudlard/character_list.html', {'characters': characters})

def character_detail(request,pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'Poudlard/character_detail.html', {'characters':character})