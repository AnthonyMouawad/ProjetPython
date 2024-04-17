def lire_mots():
    with open('listeMotsFrançais.txt', 'r', encoding='utf-8') as file:
        mots = file.read().split()
    return mots

#Faire un tableau d'occurence pour les lettres (jusqu'a 3 occurence) exemple tableau_occurence[prev_prev][prev][char] += 1
def creer_tableau_occurence(mots):
    tableau_occurence = {}
    for mot in mots:
        prev_prev = None
        prev = None
        for char in mot:
            if prev_prev not in tableau_occurence:
                tableau_occurence[prev_prev] = {}
            if prev not in tableau_occurence[prev_prev]:
                tableau_occurence[prev_prev][prev] = {}
            if char not in tableau_occurence[prev_prev][prev]:
                tableau_occurence[prev_prev][prev][char] = 1
            else:
                tableau_occurence[prev_prev][prev][char] += 1
            prev_prev = prev
            prev = char
    return tableau_occurence