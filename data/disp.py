import json
import os
from glob import glob
from files import Files
from write import Write_Files
from read import Read
from delete import Delete
from edit import Edit



class Display():
    def __init__(self, x, a): #x = l/p/t a = choix(suppr=2/lire=3/afficher=4)
        with open (Files.f_pref, 'r') as f: #charge préférence
            self.pref = json.load(f) 
        self.a = a #a = choix
        self.setup() #Vers setup
        self.list_files(x, a) #Vers list_files (x = l/p/t a = choix)
        if self.a != '5': # '5' = afficher 
            self.interact(a, x) #a = choix x = l/p/t
        
    def setup(self):
        os.makedirs(Files().chemin, exist_ok=True) #Création dossier Fichier texte si existe pas
        self.donnee = Files().verif() #Vérifie tout les fichiers dans le dossier
        Write_Files().write_json(self.donnee) #Si fichiers manquants, modifie donnee.json

    def list_files(self, x, a):
        
        if x == 'l': 
            self.liste = [i[0::4] for i in self.donnee if i[0].split("_")[0] == "losange"] #liste contenant nom fichier + si il a été deplacé
        elif x == 'p':
            self.liste = [i[0::4] for i in self.donnee if i[0].split("_")[0] == "pyramide"]
        elif x == 't':
            self.liste = [i[0::4] for i in self.donnee if i[0].split("_")[0] == "texte"]
        else: #Pour '5' (ou Afficher)
            self.liste = [i[0::4] for i in self.donnee]
        if self.pref["mode_dangereux"] == "False": #Si mode dangereux désactivé
            self.info = ['!' if i[1] == 'moved' else '' for i in self.liste]
            if a == '4' or a == '5': #4 et 5 = Lire et Afficher (tt les fichiers)
                self.id_files = [i[0].split("-")[-1].split(".")[0] for i in self.liste]
            elif a == '2' or a == '3': #2 et 3 = Supprimer et Modifier (uniquement fichiers loggés)
                self.id_files = [i[0].split("-")[-1].split(".")[0] for i in self.liste if i[1] == 'moved']   
        else: #Si mode dangereux activé
            self.id_files = [i[0].split("-")[-1].split(".")[0] for i in self.liste] #Tout les fichiers
            self.info = ['!' for i in self.liste]
        self.liste = [''.join([i[0], ' ']) if i[0].split("_")[0] == "losange" else ''.join([i[0], '   ']) if i[0].split("_")[0] == "texte" else i[0] for i in self.liste ] #Plus bel affichage
        if self.id_files != []: #Si contient qqch



            print("---------------------------------------------------")
            for i, j, k in zip(self.liste, self.id_files, self.info):
                print("| ID: {}  ||  {}  | {}".format(j, i, k))
            print("---------------------------------------------------")
        else: #Si contient rien
            print("Il n'y a rien à afficher ici.")    



    def interact(self, a, x):
        if self.id_files != []: #Si contient qqch
            self.choix = input("Veillez choisir l'identifiant du fichier ('e' pour sortir'): ")
            while self.choix not in self.id_files and self.choix != 'e': #Vérifie que c'est une ID existante 
                self.choix = input("\nVeillez choisir un identifiant de fichier valide (chiffres après 'ID: ')\nVous pouvez sortir de ce menu en écrivant 'e' (sans les guillemets): ")
            os.system('cmd /c cls')    
            if self.choix != 'e': 
                self.resultat = [i for i in self.donnee if i[1].split("-")[-1] == self.choix] #Vérifie les ID de tout les fichiers et prend les infos du fichier
                if a == '4':
                    Read().read_files(self.resultat[0], x) #Lire le fichier (resultat[0] = nom de fichier)
                elif a == '2':
                    Delete().delete_file(self.resultat[0]) #Supprime le fichier
                elif a == '3':
                    Edit().modif_file(self.resultat[0], self.donnee) #Modifie le fichier

            else:
                os.system('cmd /c cls')
        
