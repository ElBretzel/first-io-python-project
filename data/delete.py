import os
import json
from files import Files
from write import Write_Files

class Delete():
    def delete_file(self, file): #file = information du fichier

        with open (Files.f_pref, 'r') as f: #ouvre les préférences
            self.pref = json.load(f)
        if file[2] == 'losange' and file[4] == 'moved': #si fichier est un losange et qu'il est dans les logs
            file = os.path.join(Files.l_losange, file[0])
        elif file[2] == 'pyramide' and file[4] == 'moved': #si fichier est une pyramide et qu'il est dans les logs
            file = os.path.join(Files.l_pyramide, file[0])
        elif file[2] == 'texte' and file[4] == 'moved': #si fichier est un texte et qu'il est dans les logs
            file = os.path.join(Files.l_text, file[0])
        else:
            file = os.path.join(Files.chemin, file[0]) #si fichier pas dans les logs
        try:
            os.remove(file)
        except:
            print("Erreur! Fichier introuvable...")
        else:
            os.system('cmd /c cls')
            print("Le fichier à été supprimé avec succès (action irréversible)!")

    def delete_category(self):
        with open (Files.f_pref, 'r') as f: #ouvre les préférences
            self.pref = json.load(f)
        self.affichage = """
%%-----------------------------------------------------%%
|\t1: Supprimer pyramides: {} fichier(s) trouvé(s)     
|\t2: Supprimer losanges: {} fichier(s) trouvé(s)      
|\t3: Supprimer textes: {} fichier(s) trouvé(s)           
|\t4: Supprimer tout: {} fichier(s) trouvé(s)          
|\t5: Sortir                                           
%%-----------------------------------------------------%%
"""
        self.choix = ''
        while self.choix != '5':
            self.donnee = Files().verif() #vérification tout les fichiers sont présents dans les dossiers 
            Write_Files().write_json(self.donnee) #écrit les modifs dans donnee.json si pas tout les fichiers présents
            if self.pref["mode_dangereux"] == "False": #voir préférence, récupère uniquement fichiers loggés
                cp = [i for i in self.donnee if i[4] == 'moved' and i[2] == 'pyramide']
                cl = [i for i in self.donnee if i[4] == 'moved' and i[2] == 'losange']
                ct = [i for i in self.donnee if i[4] == 'moved' and i[2] == 'texte']
            else: #si mode dangereux activé, recupère tout les fichiers
                cp = [i for i in self.donnee if i[2] == 'pyramide']
                cl = [i for i in self.donnee if i[2] == 'losange']
                ct = [i for i in self.donnee if i[2] == 'texte']
            ctt = []
            ctt.extend(cp)
            ctt.extend(cl)
            ctt.extend(ct) #ctt = cp + cl + ct
            self.choix = input(self.affichage.format(len(cp), len(cl), len(ct), len(ctt)))
            os.system('cmd /c cls')

            if self.choix == '1': #suppr pyramides
                for i in cp:
                    self.delete_file(i) #renvois vers delete_file()
            elif self.choix == '2': #suppr losanges
                for i in cl:
                    self.delete_file(i)
            elif self.choix == '3': #suppr textes
                for i in ct:
                    self.delete_file(i)
            elif self.choix == '4': #suppr tout
                for i in ctt:
                    self.delete_file(i)

