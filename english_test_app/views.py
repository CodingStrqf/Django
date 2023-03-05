from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from english_test_app.form import InscriptionForm
from english_test_app.models import Joueur, Partie, Question, Verbe, Ville

# Create your views here.
def index(request):
    return render(request, "english_test_app/index.html")

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            ville = form.cleaned_data['ville']

            joueur = Joueur(nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe, idVille=ville)
            joueur.save()
            return render(request, 'english_test_app/index.html', {'form': form})

    else:
        form = InscriptionForm()
    return render(request, 'english_test_app/inscription.html', {'form': form})


