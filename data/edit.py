import os
import json
from files import Files
from pyramide import Pyramide
from write import Write_Files

class Edit():
    def PyrorLos(self, fichier):
            self.a = input("Saisissez une hauteur inférieur ou égale à 1000 pour votre {}: ".format("losange" if self.x == 'l' else "pyramide"))
            if self.a == '': #Préférence par défaut "texte_defaut"
                self.a = self.pref["longueur_defaut"]
            if self.pref["mode_dangereux"] == 'False': #Si mode dangereux désactivé
                while self.a.isdigit() == False or int(self.a) > 1000: #tant que a est un nombre inf à 1000
                    self.a = input("Erreur! Veillez choisir un nombre inférieur ou égale à 1000: ")
            self.b = input("Saisissez un signe pour votre figure: ") 
            if self.b == '':  #Préférence par défaut "caractere_defaut"
                self.b = self.pref["caractere_defaut"]
            if self.pref["mode_dangereux"] == 'False':#Si mode dangereux désactivé
                while len(self.b) != 1: #Si + d'1 caractère
                    self.b = input("Erreur! Veillez saisir un seul caractère: ")
            os.system('cmd /c cls')
            self.pyr = Pyramide().draw_pyramid(self.a, self.b, self.x) #Créer la pyramide et l'enregistre dans variable 'pyr'
            Write_Files().write_pyramide(self.pyr, self.x, fichier) #Ecrit la pyramide dans fichier texte
            return self.a
            


    def modif_file(self, file, donnee):
        with open (Files.f_pref, 'r') as f: #Charge préférence
            self.pref = json.load(f)

        if file[2] == 'pyramide' or file[2] == 'losange': #Si pyramide ou losange
            if file[2] == 'pyramide' and file[4] == 'moved': #Si pyramide loggé
                fichier = os.path.join(Files.l_pyramide, file[0]) #Chemin du fichier
                self.x = 'p' #x = 'p' (pyramide)
            elif file[2] == 'losange' and file[4] == 'moved':
                self.x = 'l'
                fichier = os.path.join(Files.l_losange, file[0])
            else: #Si mode dangereux activé
                if file[2] == 'losange':
                    self.x = 'l'
                else:
                    self.x = 'p'
                fichier = os.path.join(Files.chemin, file[0]) #Chemin fichier non loggé
            open(fichier, 'w').close() #efface le fichier
            self.a = self.PyrorLos(fichier) #fait la pyramide/ losange et enregistre hauteur dans variable a
            for i in donnee: #modifie donnee.json
                if i[0] == file[0]:
                    i[3] = self.a #modifie valeur de la hauteur dans les informations donneee
                    break
            Write_Files().write_json(donnee) #ecrit les modifications
            

        elif file[2] == 'texte': #Si texte
            if file[4] == 'moved': #si loggé
                fichier = os.path.join(Files.l_text, file[0])
            else: #si mode dangereux activé
                fichier = os.path.join(Files.chemin, file[0])
            open(fichier, 'w').close() #efface le fichier

            self.n = -1 #Variable pour indice "texte"
            self.ecrit = input("Que voulez-vous écrire ?\nPour sauter des lignes, utilisez le symbole '{}'\nPour faire un losange ou une pyramide, écrivez <losange> ou <pyramide>\n!Attention, pour mélanger du texte et des figures, veillez les séparer par un '/'!\n".format(self.pref["touche_ligne"]))
            self.ecrit = self.ecrit.split(self.pref["touche_ligne"]) #Séparé si jamais il y a texte + losange + pyramide + preferance "touche ligne"
            self.x = ['l' if self.ecrit[i].strip() == '<losange>' else 'p' if self.ecrit[i].strip() == '<pyramide>'  else 't' for i in range(len(self.ecrit))] #t /p /l
            if self.ecrit == ['']: #Préférence "texte_defaut"
                self.x = 't'
                self.ecrit = [self.pref["texte_defaut"]]
            self.ecrit = [self.ecrit[i] for i in range(len(self.ecrit)) if self.x[i] != 'l' and self.x[i] != 'p'] #texte

            for i in self.x:
                if i == 'l' or i == 'p': #Si losange ou pyramide
                    self.PyrorLos(fichier) #Vers PyrorLos()
                else:
                    self.n += 1
                    Write_Files().write_text(self.ecrit[self.n], fichier) #Ecrit le texte (ecrit[n] = indice texte de la liste 'ecrit')
        
        print("Le fichier {} à bien été modifié (action irréversible).".format(file[0]))