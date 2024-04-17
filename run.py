def lire_mots():
    with open('listeMotsFrançais.txt', 'r', encoding='utf-8') as file:
        mots = file.read().split()
    return mots

#Faire un tableau d'occurence pour les lettres (jusqu'a 3 occurence) exemple tableau_occurence[prev_prev][prev][char] += 1
def creer_tableau_occurence(mots):
    tableau_occurence = {}
    for mot in mots:
        mot = "#" + mot  # Ajoute un symbole de début de mot
        for i in range(len(mot)):
            # Obtenir le préfixe jusqu'à 3 caractères avant la lettre courante
            for j in range(3):
                if i-j < 0:
                    break
                prefix = mot[i-j:i]
                char = mot[i]
                if prefix not in tableau_occurence:
                    tableau_occurence[prefix] = {}
                if char not in tableau_occurence[prefix]:
                    tableau_occurence[prefix][char] = 0
                tableau_occurence[prefix][char] += 1

    return tableau_occurence

# Exemple d'utilisation
mots = lire_mots()
tableau_occurence = creer_tableau_occurence(mots)

# Convertir le tableau d'occurrence en JSON
import json
json_statistiques = json.dumps(tableau_occurence, ensure_ascii=False, indent=4)
print(json_statistiques)

with open('statistiques.json', 'w', encoding='utf-8') as f:
    f.write(json_statistiques)


import random

def choisir_suivant(dictionnaire):
    """ Choisir une lettre suivante basée sur les fréquences cumulatives. """
    total = sum(dictionnaire.values())
    roue = random.uniform(0, total)
    cumul = 0
    for lettre, freq in dictionnaire.items():
        cumul += freq
        if roue <= cumul:
            return lettre
    return ' '  # Retourne un espace si rien n'est trouvé (ce qui devrait être rare avec des données correctes)

def generer_mot_plausible(tableau_occurence, debut='#', longueur_min=4, longueur_max=8):
    mot = debut
    while len(mot) < longueur_max + 1:  # +1 pour le symbole initial
        prefix = mot[-3:] if len(mot) > 3 else mot[-2:] if len(mot) > 2 else mot[-1]
        if prefix not in tableau_occurence:
            break
        suivant = choisir_suivant(tableau_occurence[prefix])
        if suivant.isspace():
            if len(mot) >= longueur_min + 1:  # Vérifie si le mot a une longueur minimale
                break
            else:
                continue
        mot += suivant
    return mot[1:]  # Retourne le mot sans le symbole initial

# Génération des mots
nombre_mots = 100  # Nombre de mots à générer
mots_generes = [generer_mot_plausible(tableau_occurence) for _ in range(nombre_mots)]

# Écrire les mots dans un fichier
with open('mots_generes.txt', 'w', encoding='utf-8') as fichier:
    for mot in mots_generes:
        fichier.write(mot + '\n')
