from django.contrib import messages
from .forms import MoveForm
from .models import Character, Equipement
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

def character_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'Poudlard/character_list.html', {'characters': characters, 'equipements': equipements})

def character_detail(request,pk):
    character = get_object_or_404(Character, pk=pk)
    equipement = get_object_or_404(Equipement,id_equip=character.lieu.id_equip)
    lieu = character.lieu
    form = MoveForm()

    # Si le formulaire est soumis
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid():
            nouveau_lieu = form.cleaned_data['lieu']
            nouveau_lieu = get_object_or_404(Equipement, id_equip=nouveau_lieu)
            
            if character.etat == 'affame' and nouveau_lieu.id_equip != 'Grande Salle':
                #message "Le personnage a faim."
                messages.error(request, "Le personnage a faim.", extra_tags='danger')
                return redirect('character_detail', pk=pk)
            
            elif character.etat == 'fatigue' and nouveau_lieu.id_equip != 'Dortoir':
                #message "Le personnage a sommeil."
                messages.error(request, "Le personnage a sommeil.", extra_tags='danger')
                return redirect('character_detail', pk=pk)

            elif nouveau_lieu.disponibilite == 'occupe':
                #message "Le lieu d'arrivée est occupé. Choisissez un autre lieu."
                messages.error(request, "Le lieu d'arrivée est occupé. Choississez un autre lieu.", extra_tags='danger')
                return redirect('character_detail', pk=pk) 

            # Mise à jour du lieu d'origine
            ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()

            # Mise à jour du nouveau lieu
            if nouveau_lieu.id_equip != 'Dortoir':
                nouveau_lieu.disponibilite = "occupe"
            else:
                nouveau_lieu.disponibilite = "libre"
            nouveau_lieu.save()

            # Associer le nouveau lieu au personnage avant de sauvegarder
            character.lieu = nouveau_lieu

            # Mettre à jour l'état du personnage en fonction du lieu
            if nouveau_lieu.id_equip == 'Grande Salle':
                character.etat = 'repus'
            elif nouveau_lieu.id_equip == 'Dortoir':
                character.etat = 'affame'
            elif nouveau_lieu.id_equip in ['Foret Interdite', 'Terrain de Quidditch']:
                character.etat = 'fatigue'

            character.save()

            return redirect('character_detail', pk=character.pk)
            
    messages_warning = messages.get_messages(request)
    
    return render(request, 'Poudlard/character_detail.html', {'character': character, 'equipement': equipement, 'lieu': lieu, 'form': form, 'messages_warning': messages_warning})

def equipement_detail(request,pk):
    equipement = get_object_or_404(Equipement, pk=pk)
    characters = Character.objects.filter(lieu = equipement.id_equip)
    return render(request, 'Poudlard/equipement_detail.html', {'characters': characters, 'equipement': equipement})