import os # Importer le module os pour interagir avec le système d'exploitation (chemins de fichiers, etc.)

rep_act=os.path.dirname(__file__) # Obtenir le chemin du répertoire où se trouve ce script
fichier_seq=os.path.join(rep_act,"human-proteome.fasta") # Créer le chemin complet vers le fichier des séquences (human-proteome.fasta)
fichier_words=os.path.join(rep_act,"english-common-words.txt") # Créer le chemin complet vers le fichier des mots (english-common-words.txt)

def read_words(): # Définir une fonction pour lire les mots depuis le fichier
    liste_words=[] # Initialiser une liste vide pour stocker les mots
    with open(fichier_words, "r") as words: # Ouvrir le fichier des mots en mode lecture ("r")
        for line in words : # Parcourir chaque ligne du fichier
            word=line.strip() # Enlever les espaces et sauts de ligne au début et à la fin de la ligne
            if len(word)>=3: # Vérifier si le mot a 3 caractères ou plus
                liste_words.append(word.upper()) # Ajouter le mot en majuscules à la liste
    return liste_words # Retourner la liste des mots
    



def read_sequences(): # Définir une fonction pour lire les séquences de protéines
    sequences={} # Initialiser un dictionnaire vide pour stocker les séquences (clé=ID, valeur=séquence)
    with open(fichier_seq,"r") as sq: # Ouvrir le fichier des séquences en mode lecture
        for ligne in sq : # Parcourir chaque ligne du fichier
            if ligne.startswith(">"): # Si la ligne commence par ">", c'est un identifiant de séquence
                x=ligne.split("|") # Séparer la ligne par le caractère "|"
                cle=x[1] # Prendre la deuxième partie comme clé (l'identifiant)
                sequences[cle] = "" # Initialiser la séquence vide pour cet identifiant
            else: # Sinon, c'est une partie de la séquence elle-même
                sequences[cle] += ligne.strip() # Ajouter la ligne à la séquence en cours (sans espaces inutiles)
    return(sequences) # Retourner le dictionnaire des séquences

def search_words_in_proteome(words,sequences): # Définir une fonction pour chercher les mots dans les séquences
    resultat = {} # Initialiser un dictionnaire pour stocker les résultats (mot -> nombre d'apparitions)
    for word in words : # Pour chaque mot dans la liste des mots
        compteur = 0 # Initialiser un compteur à 0 pour ce mot
        for seq in sequences.values() : # Pour chaque séquence dans le dictionnaire des séquences
            if word in seq: # Si le mot est présent dans la séquence
                compteur+=1 # Incrémenter le compteur
        resultat[word]=compteur # Enregistrer le nombre d'apparitions pour ce mot dans le dictionnaire résultat
        if compteur > 0 : # Si le mot a été trouvé au moins une fois
            print(f"{word} trouver dans {compteur} séquences") # Afficher combien de fois il a été trouvé
    return resultat # Retourner le dictionnaire des résultats

def find_most_frequent_word(res,total_sequences): # Définir une fonction pour trouver le mot le plus fréquent
    mot_max = None # Initialiser le mot le plus fréquent à None (rien)
    max_count = 0 # Initialiser le compteur maximum à 0

    for mot , count in res.items(): # Parcourir chaque mot et son nombre d'apparitions dans les résultats
        if count > max_count : # Si le nombre d'apparitions est supérieur au maximum actuel
            max_count = count # Mettre à jour le nouveau maximum
            mot_max = mot # Mettre à jour le mot correspondant au maximum

    if mot_max is None: # Si aucun mot n'a été trouvé (mot_max est toujours None)
        print("Aucun mot trouvé dans les séquences.") # Afficher un message
        return None, 0, 0 # Retourner des valeurs vides
        
    pourcentage = (max_count / total_sequences) * 100 # Calculer le pourcentage de séquences contenant ce mot

    print(f"=> {mot_max} trouver dans {max_count} sequences") # Afficher le mot le plus fréquent et son nombre d'apparitions
    print(f"Pourcentage : {pourcentage:.2f}% des séquences") # Afficher le pourcentage calculé
    return mot_max, max_count, pourcentage # Retourner le mot, le nombre et le pourcentage

def main():
    words=read_words() # Appeler la fonction read_words et stocker le résultat dans la variable 'words'
    print(words) # Afficher la liste des mots
    print("Le nombre de mots sélectionnés :", len(words)) # Afficher le nombre total de mots sélectionnés

    proteome=read_sequences() # Appeler la fonction read_sequences et stocker le résultat dans 'proteome'
    print(proteome) # Afficher le dictionnaire des séquences (attention, ça peut être très long !)
    print(proteome.get("O95139")) # Afficher la séquence correspondant à l'identifiant "O95139" pour vérifier
    print("Le nombre de séquences lues :", len(proteome)) # Afficher le nombre total de séquences lues

    res = search_words_in_proteome(words, proteome) # Appeler la fonction de recherche et stocker le résultat dans 'res'

    find_most_frequent_word(res, len(proteome)) # Appeler la fonction pour trouver et afficher le mot le plus fréquent

if __name__ == "__main__":
    main()

                
        



