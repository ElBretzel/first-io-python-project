import os
from time import strftime
import shutil
import json
from glob import glob
from files import Files
from pyramide import Pyramide
from write import Write_Files


class AddFiles():
    def __init__(self, a, b, x, t, l): #a = hauteur b = signe x = p/l/t t = format_temps l = liste_ordonné
        self.temps = t #Format temps (créé dans fichier main.py)
        self.setup() #Vers setup
        self.create(a, b, x, l) #Vers create (#a = hauteur b = signe x = p/l/t l = liste)
        with open (Files.f_pref, 'r') as f: #Charge les préférences
            self.pref = json.load(f)
        self.organize(x) #Vers organize (x = p/l/t)
        

    def setup(self):
        os.makedirs(Files().chemin, exist_ok=True) #Création dossier 'fichier texte' si existe pas
        self.donnee = Write_Files().load_json() #charge fichier donnee.json dans variable self.donnee

    def create(self, a, b, x, l):
        if x == 'l' or x == 'p': #Uniquement si losange ou pyramide
            self.pyr = Pyramide().draw_pyramid(a, b, x) #charge une liste contenant symboles de la/le pyramide/losange (a = hauteur pyr b = signe pyr x = l/p)

        if 't' in l or ('l' in l and 'p' in l): #l = liste, vérif si il y a du texte ou il y a a la fois une pyramide et un losange
            self.fichier = Write_Files().create_file('t', a, self.temps, self.donnee) #Création du fichier avec a = hauteur (si il y a pyr/losange) temps = ID, donnee = ajout info dans donnee.json
        else:
            self.fichier = Write_Files().create_file(x, a, self.temps, self.donnee) #Si c'est pas un texte, x = l/p

        Write_Files().write_json(self.donnee) #Ecrit les informations fichiers dans donnee.json
        if x == 'l' or x == 'p':
            Write_Files().write_pyramide(self.pyr, x, self.fichier) #Ecrit pyramide si x = l/p
        else:
            Write_Files().write_text(b, self.fichier) #Ecrit texte si x = t

        self.donnee = Files().verif() #Verifis qu'aucun fichier n'a été supprimé
        Write_Files().write_json(self.donnee) #Sinon actualise donnee.json

    def move_file(self, dfile, file): #dfile= logs l/p/t file= root_l/p/t
        os.makedirs(dfile, exist_ok=True) #Création du fichier logs si n'existe pas
        shutil.move(os.path.join(Files.chemin, file), dfile) #root_l/p/t pour déplacer le fichier le plus vieux de la liste donnee.json

    def last_file(self, file):
        for l in self.donnee: #Changement du fichier déplacer de 'root' à 'moved' (méthode la moins gourmande)
            if l[0] == file: #Vérification si donnée est celui du fichier déplacé
                l[4] = 'moved'
                Write_Files().write_json(self.donnee)
                break #Casser la boucle pour éviter de prendre trop de ressource

    def organize(self, x):
        self.root =[self.donnee[i] for i in range(len(self.donnee)) if self.donnee[i][4] == 'root'] #Root = info tt fichier nn loggés
        if len(self.root) > self.pref["fichier_root"]: #Rien se passe si il y a moins de x fichiers (préférence)
            self.root_id = [self.root[i][2] for i in range(len(self.root))] #Récupère uniquement 'losange' / 'pyramide' / 'texte' (dans donnee.json)
            if self.root_id.count('losange') > self.pref["fichier_root"] and x == 'l': #Compte le nombre d'apparition du mot 'losange' dans root_id. Si en dessous de x (préférence), rien ne se passe
                self.root_l = [self.root[i][0] for i in range(len(self.root)) if self.root[i][2] == 'losange' and self.root[i][4] == 'root'] #Récupère information chemins fichiers uniquement si contient 'losange' et 'root' dans ses informations
                for i in range(len(self.root_l) - self.pref["fichier_root"]): #Si il y a plus de fichier root, fait la différence pour tous les déplacer (modif préférence)
                    self.last_file(self.root_l[i]) #modifie donnee des fichiers déplacé
                    self.move_file(Files().l_losange, self.root_l[i]) #déplace fichier(s)
            elif self.root_id.count('pyramide') >self.pref["fichier_root"] and x == 'p':
                self.root_p = [self.root[i][0] for i in range(len(self.root)) if self.root[i][2] == 'pyramide' and self.root[i][4] == 'root']
                for i in range(len(self.root_p) - self.pref["fichier_root"]):
                    self.last_file(self.root_p[i])
                    self.move_file(Files().l_pyramide, self.root_p[i])
            elif self.root_id.count('texte') >self.pref["fichier_root"] and x == 't':
                self.root_t = [self.root[i][0] for i in range(len(self.root)) if self.root[i][2] == 'texte' and self.root[i][4] == 'root']
                for i in range(len(self.root_t) - self.pref["fichier_root"]):
                    self.last_file(self.root_t[i])
                    self.move_file(Files().l_text, self.root_t[i])


#root_id[i]