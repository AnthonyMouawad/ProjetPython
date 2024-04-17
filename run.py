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
