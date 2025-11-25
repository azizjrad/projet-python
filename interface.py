from tkinter import * # Importer tout le contenu du module tkinter pour créer l'interface graphique
from tkinter import messagebox # Importer messagebox pour afficher des boîtes de dialogue (alertes, infos)
from tkinter import scrolledtext # Importer scrolledtext pour avoir une zone de texte avec barre de défilement
import threading # Importer le module threading pour exécuter l'analyse en arrière-plan sans bloquer l'interface
import words_in_proteome_lib as lib # Importer notre bibliothèque refactorisée (le fichier words_in_proteome_lib.py) sous le nom 'lib'

def run_analysis(): # Définir la fonction qui sera appelée quand on clique sur le bouton "Lancer"
    # Désactiver le bouton pour empêcher de cliquer plusieurs fois pendant que ça tourne
    B.config(state=DISABLED) # Changer l'état du bouton B à "DISABLED" (grisé/inactif)
    result_area.delete(1.0, END) # Effacer tout le contenu de la zone de résultat (de la ligne 1.0 à la fin)
    result_area.insert(END, "Analyse en cours... Veuillez patienter.\n\n") # Écrire un message d'attente dans la zone de résultat
    
    def analyze(): # Définir une fonction interne qui contient la logique de l'analyse (sera lancée dans un thread)
        try: # Commencer un bloc "try" pour gérer les erreurs éventuelles
            # 1. Lire les mots
            result_area.insert(END, "Lecture des mots...\n") # Afficher qu'on commence à lire les mots
            words = lib.read_words() # Appeler la fonction read_words de notre librairie 'lib'
            result_area.insert(END, f"{len(words)} mots lus.\n") # Afficher combien de mots ont été trouvés
            
            # 2. Lire les séquences
            result_area.insert(END, "Lecture des séquences (ça peut être long)...\n") # Prévenir que la lecture des séquences est longue
            proteome = lib.read_sequences() # Appeler la fonction read_sequences de 'lib'
            result_area.insert(END, f"{len(proteome)} séquences lues.\n") # Afficher combien de séquences ont été trouvées
            
            # 3. Chercher les mots
            result_area.insert(END, "Recherche des mots dans les séquences...\n") # Afficher qu'on commence la recherche
            res = lib.search_words_in_proteome(words, proteome) # Lancer la recherche des mots dans le protéome
            
            # 4. Trouver le plus fréquent
            result_area.insert(END, "Calcul du mot le plus fréquent...\n") # Afficher qu'on calcule le résultat final
            mot, count, percent = lib.find_most_frequent_word(res, len(proteome)) # Trouver le gagnant
            
            # Afficher les résultats
            result_area.insert(END, "\n" + "="*30 + "\n") # Ajouter une ligne de séparation
            result_area.insert(END, "RÉSULTATS\n") # Écrire le titre "RÉSULTATS"
            result_area.insert(END, "="*30 + "\n") # Ajouter une autre ligne de séparation
            
            if mot: # Si un mot a été trouvé (si 'mot' n'est pas None)
                result_area.insert(END, f"Mot le plus fréquent : {mot}\n") # Afficher le mot gagnant
                result_area.insert(END, f"Nombre d'apparitions : {count}\n") # Afficher son nombre d'apparitions
                result_area.insert(END, f"Pourcentage de séquences : {percent:.2f}%\n") # Afficher le pourcentage avec 2 chiffres après la virgule
                messagebox.showinfo("Succès", f"Analyse terminée !\nMot trouvé : {mot}") # Afficher une fenêtre pop-up de succès
            else: # Sinon (si aucun mot n'a été trouvé)
                result_area.insert(END, "Aucun mot trouvé.\n") # L'écrire dans la zone de texte
                messagebox.showwarning("Attention", "Aucun mot trouvé.") # Afficher une alerte pop-up
                
        except Exception as e: # Si une erreur se produit n'importe où dans le bloc "try"
            result_area.insert(END, f"\nErreur : {str(e)}\n") # Afficher l'erreur dans la zone de texte
            messagebox.showerror("Erreur", str(e)) # Afficher une fenêtre pop-up d'erreur
        finally: # Ce bloc s'exécute toujours à la fin, erreur ou pas
            # Réactiver le bouton
            B.config(state=NORMAL) # Remettre le bouton B à l'état "NORMAL" (cliquable)

    # Lancer l'analyse dans un thread séparé pour que l'interface ne gèle pas
    threading.Thread(target=analyze).start() # Créer et démarrer un nouveau thread qui exécute la fonction 'analyze'

main=Tk() # Créer la fenêtre principale de l'application
main.title("Analyse de Protéome") # Donner un titre à la fenêtre
main.geometry("600x500") # Définir la taille de la fenêtre (600 pixels de large, 500 de haut)

# En-tête
L1 = Label(main, text="Analyse de Mots dans le Protéome", font=("Arial", 14, "bold")) # Créer une étiquette (texte) avec une police en gras
L1.pack(pady=10) # Placer l'étiquette dans la fenêtre avec un peu d'espace vertical (pady)

# Description
L2 = Label(main, text="Cliquez sur 'Lancer' pour démarrer l'analyse.") # Créer une deuxième étiquette d'instruction
L2.pack(pady=5) # La placer en dessous avec un peu d'espace

# Cadre pour les boutons
frame_buttons = Frame(main) # Créer un conteneur (Frame) pour regrouper les boutons
frame_buttons.pack(pady=10) # Placer ce cadre dans la fenêtre

# Bouton Lancer
B = Button(frame_buttons, text="Lancer l'Analyse", command=run_analysis, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")) # Créer le bouton "Lancer" (vert, texte blanc) qui appelle 'run_analysis'
B.pack(side=LEFT, padx=10) # Le placer à gauche dans le cadre des boutons

# Bouton Quitter
B1 = Button(frame_buttons, text="Quitter", command=main.quit, bg="#f44336", fg="white", font=("Arial", 10, "bold")) # Créer le bouton "Quitter" (rouge) qui ferme l'application
B1.pack(side=RIGHT, padx=10) # Le placer à droite dans le cadre des boutons

# Zone de Résultat
result_area = scrolledtext.ScrolledText(main, width=70, height=20, font=("Consolas", 10)) # Créer une zone de texte défilante pour afficher les logs et résultats
result_area.pack(padx=10, pady=10) # La placer dans la fenêtre avec de l'espace autour

main.mainloop() # Démarrer la boucle principale de l'interface (attend les clics et événements)
