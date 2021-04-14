from write import Write_Files
from files import Files

class Pyramide():
    def draw_pyramid(self, a, b, x): #Fonction pour créer la pyramide
        self.pyr = [' '*range(int(a) + 1, 0, -1)[i] + ' '.join(b*i) for i in range (1, int(a) + 1)] #+ à - d'espace, indice i car range retourne une liste: i choisis la position + un espace entre chaque x
        for i in self.pyr: #Pyramide
            print(i) #Affichage de la pyramide sur la console
        if x is 'l': #Losange uniquement
            for i in reversed(self.pyr): #Pyramide inversé
                print(i) #Affichage d'une pyramide inversé sur la console
        print()
        return self.pyr #Retourne une pyramide
    
    
        
