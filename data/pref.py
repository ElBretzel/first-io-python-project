import os
import json
from files import Files

class Parametres():

    def par_defaut(self): #Parametre par défaut
        self.defaut = {
        "texte_defaut": "Mini éditeur de texte fait par ElBretzel",
        "longueur_defaut": "10",
        "caractere_defaut": "o",
        "mode_dangereux": "False",
        "fichier_root": 3,
        "touche_ligne": "/"
    }
        return self.defaut

    def preference(self):
        self.choix = ''
        self.fichier = Files().f_pref
        with open (self.fichier, 'r') as f: #ouvre fichier preference.json
            self.liste = json.load(f) #dans variable liste
        self.affichage = """
|----------|       
|Paramètres|
|----------|
|\t1: Texte par défaut: "{}"
|\t2: Longueur figure par défaut: "{}"
|\t3: Caractère figure par défaut: "{}"
|\t4: Debug mode: "{}"
|\t5: Limite maximum de fichier : "{}"
|\t6: Touche de saut de ligne: "{}"
|\t7: Sortir
|----------|
"""
        while self.choix != '7':
            
            self.choix = input(self.affichage.format(self.liste["texte_defaut"], self.liste["longueur_defaut"], self.liste["caractere_defaut"], self.liste["mode_dangereux"], self.liste["fichier_root"], self.liste["touche_ligne"]))
            os.system('cmd /c cls')
            with open (self.fichier, 'w') as f: #écrit modification dans fichier préférence
                json.dump(self.liste, f, indent=4)
            
            if self.choix == '1':
                self.texte = input("Que voulez-vous mettre par défaut si vous ne rentrer aucun texte ? ")
                self.liste["texte_defaut"] = self.texte #met par défaut le texte choisis de la variable 'texte'
                os.system('cmd /c cls')

            if self.choix == '2':
                self.longueur = input("Quelle valeur voulez-vous mettre par défaut si vous ne rentrer aucune longueur ? ")
                if self.liste["mode_dangereux"] == "False": #préférence
                    while self.longueur.isdigit() == False or int(self.longueur) > 1000: #tant que longueur est pas un nombre ou sup à 1000
                        self.longueur = input("Erreur! Veillez choisir un nombre inférieur ou égale à 1000: ")
                self.liste["longueur_defaut"] = self.longueur #met par défaut la longueur
            
            if self.choix == '3':
                self.car = input("Quel caractère voulez-vous mettre par défaut si vous ne rentrer aucun symbole ? ")
                if self.liste["mode_dangereux"] == "False": #préférence
                    while len(self.car) != 1: #si plus d'un caractère
                        self.car = input("Erreur! Veillez saisir un seul caractère: ")
                self.liste["caractere_defaut"] = self.car #met par défaut
            
            if self.choix == '4': #change mode dangereux en True si False et renversement
                if self.liste["mode_dangereux"] == 'False':
                    self.liste["mode_dangereux"] = 'True'
                else:
                    self.liste["mode_dangereux"] = 'False'

            if self.choix == '5': #change le nombre de fichier avant d'etre loggé (compris entre 1 et 5)
                if self.liste["fichier_root"] < 5: #si inf à 5
                    self.liste["fichier_root"] += 1 #rajoute 1
                else:
                    self.liste["fichier_root"] = 1 #si 5, passe à 1
            if self.choix == '6':
                self.signe = input("Quel caractère voulez-vous choisir pour sauter une ligne ? ")
                if self.liste["mode_dangereux"] == "False": #préférence
                    while len(self.signe) != 1: #si plus d'un caractère
                        self.signe = input("Erreur! Veillez saisir un seul caractère: ")
                self.liste["touche_ligne"] = self.signe

            if self.choix == '00': #affiche chemin d'installation
                print("Chemin vers dossier installation: {}\nChemin vers les fichiers textes stockés: {}\n\nChemin d'accès vers les logs (si existent):\nPyramide: {}\nLosange: {}\nTexte: {}".format(''.join(os.path.dirname(__file__).split("\data")[0]), Files().chemin, Files().l_pyramide, Files().l_losange, Files().l_text))

            if self.choix == '0': #remet parametre par défaut
                self.defaut = self.par_defaut()
                with open (self.fichier, 'w') as f: #réecrit fichier préférence
                    json.dump(self.defaut, f, indent=4)
                self.liste = self.defaut #met par défaut
