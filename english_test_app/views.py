from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from english_test_app.form import InscriptionForm
from english_test_app.models import Joueur, Partie, Question, Verbe, Ville
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json

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

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            joueur = Joueur.objects.get(email=email)
        except Joueur.DoesNotExist:
            joueur = None
        if joueur is not None and password == joueur.mot_de_passe:
            messages.success(request, "Vous êtes maintenant connecté !")
            
            url = reverse('jeu') + f'?email={email}'
            return redirect(url)
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'english_test_app/index.html')


def jeu(request):
    # Récupération du joueur connecté
    #print("request ", email)
    print(request.GET)
    
    
    if request.method == 'POST':
        # Récupération de la réponse de l'utilisateur
        json_data = json.loads(getTime())

        
        preterit = request.POST.get('preterit')
        participe_passe = request.POST.get('participe_passe')
        
        question_index = request.session.get('question_index')
        joueur = Joueur.objects.get(id=request.session.get('joueur'))
        partie = Partie.objects.get(id=request.session.get('partie'))
        AnciennePartie = Partie.objects.get(id=request.session.get('anciennePartie'))
        
        question = Question.objects.get(id=question_index)
        print(request.session.get('verbe'))
        verbe = Verbe.objects.get(baseVerbal=request.session.get('verbe'))
        # Vérification de la réponse

        if json_data['time'] - json.loads(request.session.get('time'))['time'] >= 60 :
            context = { 'message': "GAGNE", 'question_index': question_index, 'verbe': verbe.baseVerbal }
            return render(request, 'english_test_app/fin.html', context=context)

        is_correct = (preterit == verbe.preterit and participe_passe == verbe.participePasse)
        #is_correct = True
        print(is_correct , verbe.baseVerbal, verbe.preterit, verbe.participePasse)
        if is_correct:
            if question_index == 10:
                # Redirection vers la vue de fin de partie
                context = { 'message': "GAGNE", 'question_index': question_index, 'verbe': verbe.baseVerbal }
                return render(request, 'english_test_app/fin.html', context=context)
            # Mise à jour de la variable de session pour passer à la question suivante
            print('correct')
            question = Question.objects.order_by('?')[0] 
            
            request.session['question_index'] = question_index + 1
            verbe = Verbe.objects.get(baseVerbal=question.idVerbe)
            request.session['time'] = getTime()

            message = "Bravo"
        else:
            # Redirection vers la même vue pour afficher la même question
            #return render(request, 'english_test_app/jeu.html',context=)
            question = None
            message = "Perdu"
            context = { 'message': "GAGNE", 'question_index': question_index, 'verbe': verbe, 'number': request.session.get('question_index') }
            return render(request, 'english_test_app/fin.html', context=context)

    else : 
        message = "Bravo"
        question = Question.objects.order_by('?')[0]        
        verbe = Verbe.objects.get(baseVerbal=question.idVerbe)
        email = request.GET.get('email')
        if email is None:
            joueur = Joueur.objects.get(id= request.session.get('joueur'))
        else :
            joueur = Joueur.objects.get(email=email)

        # Récupération de la dernière partie du joueur
        if Partie.objects.filter(idJoueur=joueur).count() > 0:
            AnciennePartie = Partie.objects.filter(idJoueur=joueur).order_by('-id')[0]
        else :
            AnciennePartie = None 
        partie = Partie(idJoueur=joueur)
        partie.save()

        # Passer les informations à la template
        request.session['question_index'] = 1
        request.session['joueur'] = joueur.id
        request.session['partie'] = partie.id
        request.session['anciennePartie'] = AnciennePartie.id
        request.session['verbe'] = verbe.baseVerbal

        request.session['time'] = getTime()
    context = {
        'joueur': joueur,
        'partie': partie,
        'anciennePartie': AnciennePartie,
        'questions': question,
        'verbe': verbe,
        'message': message,
        'nbr': request.session.get('question_index')
    }
    return render(request, 'english_test_app/jeu.html', context)

def fin(request):
    joueur = Joueur.objects.get(id=request.session.get('joueur'))
    partie = Partie.objects.get(id=request.session.get('partie'))
    AnciennePartie = Partie.objects.get(id=request.session.get('anciennePartie'))
    verbe = Verbe.objects.get(baseVerbal=request.session.get('verbe'))
    number = request.session.get('question_index')
    print("number :", number)
    print("laaaaaaaaaaaaaaaaa")
    context = {
        'joueur': joueur,
        'partie': partie,
        'anciennePartie': AnciennePartie,
        'verbe': verbe,
        'number': number,
    }
    return render(request, 'english_test_app/fin.html', context)

def getTime():
        my_time = datetime.datetime.now()
        time_string = my_time.strftime('%H%M%S')
        json_data = json.dumps({'time': int(time_string)}, cls=DjangoJSONEncoder)
        return json_data