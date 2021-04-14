import json
import files
import os

class Write_Files():
    def load_json(self): #Charges informations contenu dans donnee.json
        with open (files.Files.f_json, 'r') as f:
            self.donnee = json.load(f)
        return self.donnee
    
    def write_json(self, donnee): #Pour écrire les informations dans un fichiers json
        if len(donnee) > 1: #Si longueur donnee supérieur a 1 
            if donnee[-1][0] == donnee[len(donnee)-2][0]: #Si les donnees sont les mêmes
                donnee.pop(-1) #suppr la dernière 
        with open (files.Files.f_json, 'w') as f:
            json.dump(donnee, f, indent=4) #Mets a jour informations
    
    def create_file(self, x, a, temps, donnee):
        
        if x == 'p': #Pyramide
            self._files = os.path.join(files.Files.chemin, 'pyramide_{}.txt'.format(temps)) #Création fichier 'pyramide.txt' avec pour ID le temps
            donnee.append([self._files.split("\\")[-1], str(temps), self._files.split("\\")[-1].split("_")[0], a, "root"]) #Différentes méta-données
        elif x == 'l': #Losange
            self._files = os.path.join(files.Files.chemin, 'losange_{}.txt'.format(temps))
            donnee.append([self._files.split("\\")[-1], str(temps), self._files.split("\\")[-1].split("_")[0], a, 'root'])
        elif x == 't':
            self._files = os.path.join(files.Files.chemin, 'texte_{}.txt'.format(temps))
            donnee.append([self._files.split("\\")[-1], str(temps), self._files.split("\\")[-1].split("_")[0], a, 'root'])  
        return self._files
    
    def write_pyramide(self, pyr, x, file):
        self.seq = [] #seq va être une liste utilisé lors de l'écriture du fichier texte
        for i in pyr: #Pyramide 
            self.seq.append(i + '\n') #Ajout d'un schéma (x = signe) + saut de ligne dans une liste 'seq'
        if x == 'l': #Losange
            for i in reversed(pyr): #Pyramide inversé
                self.seq.append(i + '\n')
        with open (file, 'a') as f:
            f.writelines(self.seq) #Ecrit la séquence dans un fichier texte grâce à la liste seq
        
    def write_text(self, t, file): #Si c'est un texte
        with open (file, 'a') as f:
            f.write("{}\n".format(t)) #Ecrit le texte dans un fichier texte

