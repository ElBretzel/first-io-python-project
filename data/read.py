import os
import json
from files import Files

class Read():   
    def read_files(self, file, x): 
        with open (Files.f_pref, 'r') as f: #préférence
            self.pref = json.load(f)
        self.donnee = file #car file va être modifié
        if file[2] == 'losange' and file[4] == 'moved':
            file = os.path.join(Files.l_losange, file[0]) #file devient un chemin 
        elif file[2] == 'pyramide' and file[4] == 'moved':
            file = os.path.join(Files.l_pyramide, file[0])
        elif file[2] == 'texte' and file[4] == 'moved':
            file = os.path.join(Files.l_text, file[0])
        else:
            file = os.path.join(Files.chemin, file[0]) #si fichier pas dans les logs
        try:
            with open(file, 'r') as f: #lis le fichier
                self.contenu = f.read()
        except:
                print("Erreur! Fichier introuvable...")
        else:    
            os.system('cmd /c cls')
            liste = [0, 2, 4, 6]
            self.date = [self.donnee[1].split("-")[i] for i in range(3)] #affiche la date
            self.heure = [self.donnee[1].split("-")[-1][liste[i]:liste[i+1]] for i in range(3)] #affiche l'heure de création
            if self.pref["mode_dangereux"] == 'False': #preference
                if self.donnee[3] == 'None' or int(self.donnee[3]) > 100: #si fichier texte ou taille pyramide / losange supérieur à 100
                    erreur = input("Attention, lecture dangereuse, le fichier peut être volumineux et lent à ouvrir.\nL'ouvrir quand même ('O' / 'N') ? ")
                    if erreur == 'O':
                        print(self.contenu) #affiche le contenu si on choisis 0
                    else:
                        print("Lecture annulée") 
                else:
                    print(self.contenu) #Si pas un fichier texte et taille pyramide / losange inférieur à 100
            else:
                print(self.contenu) #Si mode dangereux activé

            print("\nNom du fichier: {}".format(self.donnee[0]))
            print("Date de création: {}/{}/{} à {}h:{}m:{}s".format(self.date[2], self.date[1], self.date[0], self.heure[0], self.heure[1], self.heure[2]))
            print("Type de fichier: {}".format(self.donnee[2]))
            if x == 'l' or x == 'p': #Si pyramide ou losange
                print("Hauteur de le/la {}: {}\n".format(self.donnee[2], int(self.donnee[3])*2 if x == 'l' else self.donnee[3]))