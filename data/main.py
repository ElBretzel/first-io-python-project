import os
import json
from files import Files
from add import AddFiles
from disp import Display
from time import strftime
from pref import Parametres
from delete import Delete

choix = ''
affichage = """
    **Editeur de texte**
|-------------------------|
|\t1: Ajouter        |
|\t2: Supprimer      |
|\t3: Modifier       |
|\t4: Lire           |
|\t5: Afficher       |
|\t6: Paramètre      |
|\t7: Sortir         |
|-------------------------|
"""

if not os.path.exists(Files.f_json): #Vérification fichier donnee.json existe, sinon en créer un
    with open (Files.f_json, 'w') as f:
        json.dump([], f)
if not os.path.exists(Files.f_pref): #Vérification fichier preference.json existe, sinon en créer un + parametre par défaut
    defaut = Parametres().par_defaut() #Paramètre par défaut
    with open (Files.f_pref, 'w') as f:
        json.dump(defaut, f, indent=4)

while choix != '7':
    choix = input(affichage)
    os.system('cmd /c cls') #Execute une commande prompt pour clear la console
    
    if choix == '1': #Choix 1 == Ajouter
        with open (Files.f_pref, 'r') as f: #Ouvre fichier json préférence pour plus tard
            pref = json.load(f)
        temps = strftime(r"%Y-%m-%d-%H%M%S") #ID (l'ID sera toujours croissante)
        n = -1 #Variable pour indice "texte"

        ecrit = input("Que voulez-vous écrire ?\nPour sauter des lignes, utilisez le symbole '{}'\nPour faire un losange ou une pyramide, écrivez <losange> ou <pyramide>\n!Attention, pour mélanger du texte et des figures, veillez les séparer par un '/'!\n".format(pref["touche_ligne"]))
        ecrit = ecrit.split(pref["touche_ligne"]) #Séparé si jamais il y a texte + losange + pyramide + preferance "touche signe"
        x = ['l' if ecrit[i].strip() == '<losange>' else 'p' if ecrit[i].strip() == '<pyramide>'  else 't' for i in range(len(ecrit))] #Retourne t/p/l selon ordre donné dans 'ecrit'
        if ecrit == ['']: #Préférence par défaut "texte_defaut"
            x = 't' #Initialise directement en texte
            ecrit = [pref["texte_defaut"]]
        ecrit = [ecrit[i] for i in range(len(ecrit)) if x[i] != 'l' and x[i] != 'p'] #Retourne le texte
        os.system('cmd /c cls') #Clear console
        for i in x:
            if i == 'l' or i == 'p':
                a = input("Saisissez une hauteur inférieur ou égale à 1000 pour votre {}: ".format("losange" if i == 'l' else "pyramide"))
                if a == '': #Préférence défaut "longueur_defaut"
                    a = pref["longueur_defaut"]
                if pref["mode_dangereux"] == 'False': #Si mode dangereux désactivé
                    while a.isdigit() == False or int(a) > 1000: #Si 'a' pas un nombre ou sup à 1000
                        a = input("Erreur! Veillez choisir un nombre inférieur ou égale à 1000: ")
                b = input("Saisissez un signe pour votre figure: ") 
                if b == '': #Préférence défaut "caractere_defaut"
                    b = pref["caractere_defaut"]
                if pref["mode_dangereux"] == 'False':
                    while len(b) != 1: #Si 'b' ne contient plus d'1 caractère
                        b = input("Erreur! Veillez saisir un seul caractère: ")
                os.system('cmd /c cls') #Execute une commande prompt pour clear la console
                a = AddFiles(a, b, i, temps, x) #a = hauteur b = signe i = p/l/t temps = format_temps x = liste
            else:
                os.system('cmd /c cls')
                n += 1 #Indice texte dans la liste 'ecrit'
                a = AddFiles('None', ecrit[n] ,i , temps, x) #ecrit[n] = texte, i = t temps = format_temps x = liste
        print("Le fichier contenant votre choix a été créé.")
                

    elif choix == '2':
        x = input("Voulez-vous supprimer les fichiers sur les pyramides (p) / les losanges (l) ou les textes (t) ?\nPour supprimer toute une catégorie de fichier, rentrer 'tout'\nUn fichier contenant du texte et une figure ou plusieurs figures ou que du texte sera considéré comme fichier texte. ")
        while x != "p" and x != "l" and x != "t" and x != "tout": #tant que x n'est pas p / l / t / tout
            x = input("Erreur! Pour choisir de voir les pyramides, rentrez 'p', les losanges 'l' ou les textes 't' ou une catégorie de fichier 'tout' (sans les guillemets): ")
        os.system('cmd /c cls') #Execute une commande prompt pour clear la console
        if x == "p" or x == "l" or x == "t": #Si x est soit p / l / t
            r = Display(x, choix) #x = l/t/p/tout choix= '2' (pour suppr) 
        else:
            Delete().delete_category() #Si x est 'tout' (suppr les catégorie)


    elif choix == '3':
        x = input("Voulez-vous modifier les fichiers sur les pyramides (p) / les losanges (l) ou les textes (t) ?\nUn fichier contenant du texte et une figure ou plusieurs figures ou que du texte sera considéré comme fichier texte. ")
        while x != "p" and x != "l" and x != "t":
            x = input("Erreur! Pour choisir de modifier les pyramides, rentrez 'p' ou les losanges 'l' ou les textes 't' (sans les guillemets): ")
        os.system('cmd /c cls')
        r = Display(x, choix) #x = l/t/p #choix = '3' (pour modif)

    elif choix == '4':
        x = input("Voulez-vous lire les fichiers sur les pyramides (p) / les losanges (l) ou les textes (t) ?\nUn fichier contenant du texte et une figure ou plusieurs figures ou que du texte sera considéré comme fichier texte. ")
        while x != "p" and x != "l" and x != "t": #tant que x n'est pas p / l / t
            x = input("Erreur! Pour choisir de voir les pyramides, rentrez 'p' ou les losanges 'l' ou les textes 't' (sans les guillemets): ")
        os.system('cmd /c cls')
        r = Display(x, choix) #x = l/t/p choix = '4' (pour lire)

    elif choix == '5':
        os.system('cmd /c cls') #Execute une commande prompt pour clear la console
        r = Display('None', choix) #choix = '5' (pour afficher tout)

    elif choix == '6':
        Parametres().preference() #Vers menu des préférences

