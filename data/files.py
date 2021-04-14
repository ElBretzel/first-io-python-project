import os
from glob import glob
from write import Write_Files

class Files:
    chemin = os.path.join(''.join(os.path.dirname(__file__).split("\data")[0]), 'Fichier texte') #Chemin dossier 'fichier texte'
    f_json = os.path.join(os.path.dirname(__file__), 'donnee.json') #Chemin fichier 'donnee.json'
    f_pref = os.path.join(os.path.dirname(__file__), 'preference.json') #Chemin fichier 'donnee.json'
    l_pyramide = os.path.join(chemin, 'Logs pyramides') #Chemin dossier 'logs pyramides'
    l_losange = os.path.join(chemin, 'Logs losanges') #Chemin dossier 'logs losanges'
    l_text = os.path.join(chemin, 'Logs textes') #Chemin dossier 'logs textes'
    fichier = glob(os.path.join(chemin, "**"), recursive=True) #tout les fichiers existants

    def verif(self):
        self.donnee = Write_Files().load_json()
        self.fichier = glob(os.path.join(Files.chemin, "**"), recursive=True) #Besoin d'update
        self.liste = [self.fichier[i].split("\\")[-1] for i in range(len(self.fichier))] #Nom complet de tout fichiers txt
        self.donnee = [i for i in self.donnee if i[0] in self.liste] #Vérification si le fichier à été supprimé  
        return self.donnee

