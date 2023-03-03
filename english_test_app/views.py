from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from english_test_app.form import InscriptionForm
from english_test_app.models import Joueur, Partie, Question, Verbe, Ville

# Create your views here.
def index(request):
    return render(request, "english_test_app/index.html")

def inscription(request):

    if (request.method == 'POST'):
        print("POST")
        form = InscriptionForm(request.POST)

        if form.is_valid():
            nom = form['nom']
            prenom = form['prenom']
            email = form['email']
            mot_de_passe = form['mot_de_passe']
            ville = form['ville']
        
            joueur = Joueur(nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe, ville=ville)
            joueur.save()

            request.session['joueur_id'] = joueur.id
            return redirect(index)
        else:
            print(form.errors)
    else:
        form = InscriptionForm()

    return render(request, "english_test_app/inscription.html", {
        'form':form
    })