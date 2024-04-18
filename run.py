import json
import random
import os

#Ouverture du fichier texte contenant les mots français
def lire_mots():
    with open('listeMotsFrançais.txt', 'r', encoding='utf-8') as file:
        mots = file.read().split()
    return mots

n = int(input("Profondeur mots à afficher: "))

#Tableau d'occurence pour les lettres (jusqu'a 3 occurences)
def creer_tableau_occurence(mots):
    tableau_occurence = {}
    for mot in mots:
        mot_traité = "#" + mot + "$"  # Ajoute un symbole de début et de fin de mot
        for i in range(len(mot_traité)):
            for j in range(1, n):  # On prend en compte maintenant jusqu'à 4 caractères pour le préfixe
                if i-j < 0:
                    break
                prefix = mot_traité[i-j:i]
                char = mot_traité[i]
                if prefix not in tableau_occurence:
                    tableau_occurence[prefix] = {}
                if char not in tableau_occurence[prefix]:
                    tableau_occurence[prefix][char] = 0
                tableau_occurence[prefix][char] += 1
    return tableau_occurence


mots = lire_mots()
tableau_occurence = creer_tableau_occurence(mots)
print("Statisiques occurences en cours de génération...")
# Convertir le tableau d'occurrence en JSON
json_statistiques = json.dumps(tableau_occurence, ensure_ascii=False, indent=4)
with open('statistiques.json', 'w', encoding='utf-8') as f:
    f.write(json_statistiques)

# Fonction pour choisir la lettre suivante basée sur la distribution des probabilités
def choisir_suivant(dictionnaire):
    total = sum(dictionnaire.values())
    roue = random.uniform(0, total)
    cumul = 0
    for lettre, freq in dictionnaire.items():
        cumul += freq
        if roue <= cumul:
            return lettre
    return ' '  # Retourne un espace si rien n'est trouvé

# Faire un input pour choisir la longueur minimale et maximale des mots
longueur_min = int(input("Longueur minimale des mots: "))

def generer_mot_plausible(tableau_occurence, longueur_min, longueur_max = 100):
    mot = '#'
    while True:
        prefix = mot[-4:] if len(mot) > 4 else mot
        if prefix not in tableau_occurence:
            break
        suivant = choisir_suivant(tableau_occurence[prefix])
        if suivant == '$':  # Si le symbole suivant est le symbole de fin de mot
            if len(mot) - 1 >= longueur_min:
                break  # Finir le mot si la longueur minimale est atteinte
            else:
                mot = '#'  # Sinon, recommencer
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
print("Mots générés avec succès!")

#Ouvrir le fichier contenant les mots générés
os.startfile("mots_generes.txt")