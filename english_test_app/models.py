from django.db import models

class Ville(models.Model):
    cp = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom
    
class Joueur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    prenom = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=20)
    niveau = models.CharField(max_length=100)
    idVille = models.ForeignKey('Ville', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.nom
    
class Partie(models.Model):
    idJoueur = models.ForeignKey('Joueur', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.idJoueur
    
class Question(models.Model):
    idPartie = models.ForeignKey('Partie', on_delete=models.PROTECT, null=True)
    idVerbe = models.ForeignKey('Verbe', on_delete=models.PROTECT, null=True)
    reponsePreterit = models.CharField(max_length=100)
    reponseParticipePasse = models.CharField(max_length=100)
    dateEnvoi = models.DateTimeField()
    dateReponse = models.DateTimeField()
    def __str__(self):
        return self.idPartie
    
class Verbe(models.Model):
    baseVerbal = models.CharField(max_length=100)
    preterit = models.CharField(max_length=100)
    participePasse = models.CharField(max_length=100)
    traduction = models.CharField(max_length=100)
    def __str__(self):
        return self.baseVerbal