from time import *
import random
import math
import sys

sys.setrecursionlimit(5000)

def affiche_tableau(tableau):
    for n in range(len(tableau)):
        print(" ", tableau[n])

def echange(liste, n , p):
    temp = liste[n]
    liste[n] = liste[p]
    liste[p] = temp

def genere_arrangement(n, nb):
    l_realisation = [0] * n
    liste_tire = [0] * nb
    for i in range(len(liste_tire)):
        liste_tire[i] = i
    nb_tire = 0
    i = 0
    nb_alea = 0
    for i in range(n):
        nb_alea = random.randint(nb_tire, nb -1)
        echange(liste_tire, i , nb_alea)
        nb_tire += 1
        l_realisation[i] = liste_tire[i]
    return l_realisation

def taquin_to_liste(taquin):
    liste = [0] * len(taquin) * len(taquin[0])
    for i in range(len(taquin)):
        for j in range(len(taquin[0])):
            liste[i * len(taquin[0]) + j] = taquin[i][j]
    return(liste)

def genere_tirage_aleatoire(liste_evenement, liste_proba, nb_resultat):
    l_realisation = [0] * nb_resultat
    proba_cumul = [0] * len(liste_proba)
    nb_alea = 0
    proba_cumul[0] = liste_proba[0]
    for i in range(len(liste_proba)-1):
        proba_cumul[i+1] = proba_cumul[i] + liste_proba[i+1]

    for i in range(nb_resultat):
        nb_alea = random.uniform(0, 1)
        for j in range(len(proba_cumul)):
            if(nb_alea < proba_cumul[j]):
                l_realisation[i] = liste_evenement[j]
                break
    return l_realisation

def liste_to_taquin(liste, n, p):
    temp = [0] * p
    taquin = [0] * n
    for i in range(n):
        taquin[i] = temp[:]
    for i in range(n):
        for j in range(p):
            taquin[i][j] = liste[i * p + j]
    return(taquin)

def parite_taquin(taquin):
    colonne = len(taquin[0])
    liste = taquin_to_liste(taquin)
    index_0 = liste.index(0)
    parite_case = index_0%colonne + (int)(index_0/colonne)
    compteur = 0
    for i in range(len(liste)):
        indice = liste.index(i)
        if indice != i:
            echange(liste, indice, i)
            compteur = compteur + 1
    return (parite_case + compteur)

def valide_taquin(taquin):
    parite = parite_taquin(taquin)
    if (parite%2 == 0):
        return 1
    else:
        return 0

def random_taquin(n, p):
    liste_evenement = [0] * n * p
    for i in range(n * p):
        liste_evenement[i] = i
    liste = genere_arrangement(n * p, n * p)
    return(liste_to_taquin(liste, n, p))

def cree_taquin(n, p):
    parite = 0
    while(parite == 0):
        taquin = random_taquin(n, p)
        temp = taquin[:]
        parite = valide_taquin(temp)
    return (taquin)

def compte_taquin(taquin):
    compteur = 0
    for i in range(len(taquin)):
        for j in range(len(taquin[0])):
            if taquin[i][j] != 0:
                ligne = (int)(taquin[i][j]/len(taquin[0]))
                colonne = taquin[i][j]%len(taquin[0])
                decalage_ligne = abs(ligne - i)
                decalage_colonne = abs(colonne - j)
                compteur = (decalage_ligne + decalage_colonne) * taquin[i][j] * 1 + compteur#
    return compteur

def deplacement_possible_taquin(taquin, ligne_bloque):
    ligne = len(taquin)
    colonne = len(taquin[0])
    liste = taquin_to_liste(taquin)
    indice_vide = liste.index(0)
    deplacement = [0] * 4
    resultat = []
    for i in range(4):
        #interpolation de lagrange
          # f(x) = (-x³ + 3x² + x)/3 - 1
        deplacement_verticale = (int)((-pow(i, 3) + 3 * pow(i, 2) + i)/3 - 1) * colonne
          # f(x) = (x³ - 6x² + 8x)/3
        deplacement_horizontale = (int)((pow(i, 3) - 6 * pow(i, 2) + 8 * i )/3)
        deplacement[i] = (deplacement_horizontale + deplacement_verticale) + indice_vide
    if (indice_vide < colonne): # case vide sur le haut du taquin
        deplacement[0] = -1
    if (indice_vide%colonne == colonne-1): # case vide sur la droite du taquin
        deplacement[1] = -1
    if (ligne_bloque * colonne - indice_vide - 1 < colonne): # case vide sur le bas du taquin
        deplacement[2] = -1
    if (indice_vide%colonne == 0): # case vide sur la gauche du taquin
        deplacement[3] = -1
    for i in range(4):
        temp = liste[:]
        if(deplacement[i] != -1):
            echange(temp, indice_vide, deplacement[i])
            resultat.append(liste_to_taquin(temp, ligne, colonne))
    return (resultat)

def resolution_taquin(taquin, bonus):
    ligne = len(taquin)
    colonne = len(taquin[0])
    compteur = 0
    ligne_bloque = ligne
    taquin_finale = [0] * ligne * colonne
    for i in range(len(taquin_finale)):
        taquin_finale[i] = i
    taquin_finale = liste_to_taquin(taquin_finale, ligne, colonne)

    while(taquin_finale != taquin):
        deplacement_possible = deplacement_possible_taquin(taquin, ligne_bloque)
        nb_deplacement = len(deplacement_possible)
        compte = [0] * nb_deplacement
        meilleur = [0, compte_taquin(deplacement_possible[0])]
        for i in range(len(compte)):
            compte[i] = compte_taquin(deplacement_possible[i])
            if (compte_taquin(deplacement_possible[i]) < meilleur[1]):
                meilleur = [i, compte_taquin(deplacement_possible[i])]
        liste_evenement = [0] * nb_deplacement
        for i in range(nb_deplacement):
            liste_evenement[i] = i
        liste_proba = [1/(nb_deplacement + bonus)] * nb_deplacement
        liste_proba[meilleur[0]] = (bonus + 1)/(nb_deplacement + bonus)
        deplacement_choisi = genere_tirage_aleatoire(liste_evenement, liste_proba, 1)
        taquin = deplacement_possible[deplacement_choisi[0]][:]

        compteur = compteur + 1
        if (taquin[ligne_bloque - 1] == taquin_finale[ligne_bloque - 1]):
            ligne_bloque = max(ligne_bloque - 1, 2)
    return (compteur)


bonus_debut = 1
bonus_fin = 4
repetition = 100
resultat = []
for bonus in range(bonus_debut, bonus_fin + 1):
    tempres = []
    somme = 0
    for i in range(repetition):
        print("  Bonus", bonus, "  Repetition", i)
        temp = cree_taquin(5, 4)
        nb_deplacement = resolution_taquin(temp, bonus)
        somme = somme + nb_deplacement
    resultat.append(["bonus", bonus, "moyenne", somme/repetition])
affiche_tableau (resultat)
