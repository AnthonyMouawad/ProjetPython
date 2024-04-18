import json
import random
import os

# Suppression des fichiers de sauvegarde si ils existent
if os.path.exists("mots_generes.txt"):
    os.remove("mots_generes.txt")

if os.path.exists("occurences.json"):
    boolChoiceOccurences = input('Voulez vous garder les occurences acutelles ? oui ou non ') # Demande si l'utilisateur veut garder les occurences actuelles
    if (boolChoiceOccurences == "non"): # Si l'utilisateur ne veut pas garder les occurences actuelles alors on supprime
        os.remove("occurences.json")
        print("Occurences supprimées")
    elif (boolChoiceOccurences == "oui"): # Si l'utilisateur veut garder les occurences actuelles alors on garde
        print("Occurences gardées")

# Ouverture du fichier texte contenant les mots en français
def lire_mots():
    with open('listeMotsFrançais.txt', 'r', encoding='utf-8') as file:
        mots = file.read().split() # Séparer les mots par les espaces
    return mots

# Input pour choisir la profondeur des mots à afficher
n = int(input("Profondeur mots à afficher: "))

# Tableau d'occurence pour les lettres
def creer_tableau_occurence(mots):
    tableau_occurence = {}
    for mot in mots:
        mot_traité = "#" + mot + "$"  # Ajoute un symbole de début et de fin de mot
        for i in range(len(mot_traité)):
            for j in range(1, n):  # On prend en compte maintenant jusqu'à n caractères pour le préfixe
                if i-j < 0: # Si on dépasse le début du mot, on arrête
                    break
                prefix = mot_traité[i-j:i] # Préfixe de longueur j
                char = mot_traité[i] # Caractère suivant
                if prefix not in tableau_occurence:
                    tableau_occurence[prefix] = {} # Crée un dictionnaire vide pour le préfixe
                if char not in tableau_occurence[prefix]:
                    tableau_occurence[prefix][char] = 0 # Initialise le compteur à 0
                tableau_occurence[prefix][char] += 1 # Incrémente de +1 le compteur
    return tableau_occurence

# Lire les mots
mots = lire_mots()

# Charger les occurences depuis le fichier JSON si il existe
if os.path.exists("occurences.json"):
    # Lire le fichier JSON
    with open('occurences.json', 'r', encoding='utf-8') as file:
        tableau_occurence = json.load(file)
else:
    # Créer le tableau d'occurences
    print('Occurences en cours de création...')
    tableau_occurence = creer_tableau_occurence(mots)

# Convertir le tableau d'occurrence en JSON
json_occurences = json.dumps(tableau_occurence, ensure_ascii=False, indent=4)
with open('occurences.json', 'w', encoding='utf-8') as f:
    f.write(json_occurences)

# Fonction pour choisir la lettre suivante basée sur la distribution des probabilités
def choisir_suivant(dictionnaire):
    total_dictionnaire = sum(dictionnaire.values()) # Somme des fréquences
    val = random.uniform(0, total_dictionnaire) # Valeur aléatoire entre 0 et la somme des fréquences
    cumul = 0
    for lettre, freq in dictionnaire.items():
        cumul += freq # Cumul des fréquences
        if val <= cumul: # Si la valeur aléatoire est inférieure ou égale au cumul
            return lettre
    return ' '  # Retourne un espace si rien n'est trouvé

# Input pour choisir la longueur minimale et maximale des mots
longueur_min = int(input("Longueur minimale des mots: "))

def generer_mot_plausible(tableau_occurence, longueur_min, longueur_max = 100):
    mot = '#'
    while True:
        prefix = mot[-4:] if len(mot) > 4 else mot # Prend les 4 dernières lettres du mot
        if prefix not in tableau_occurence:
            break
        suivant = choisir_suivant(tableau_occurence[prefix])
        if suivant == '$':  # Si le symbole suivant est le symbole de fin de mot
            if len(mot) - 1 >= longueur_min:
                break  # Finir le mot si la longueur minimale est atteinte
            else:
                mot = '#'  # Recommencer si la longueur minimale n'est pas atteinte
                continue
        mot += suivant
        if len(mot) - 1 == longueur_max:
            break
    return mot[1:]  # Omettre le symbole initial pour retourner le mot final


# Génération des mots
nombre_mots = int(input("Nombre de mots à générer: "))
mots_generes = [generer_mot_plausible(tableau_occurence, longueur_min) for _ in range(nombre_mots)]

# Écrire les mots dans un fichier
with open('mots_generes.txt', 'w', encoding='utf-8') as fichier:
    for mot in mots_generes:
        fichier.write(mot + '\n')
print("Mots générés")

# Ouvrir le fichier contenant les mots générés
os.startfile("mots_generes.txt")