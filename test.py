col = {0:[0], 1:[0], 2:[0], 3:[0], 4:[0]}

matrice = [[1,1,1,1,1],
           [0,1,1,1,0],
           [0,1,0,1,1],
           [0,1,0,1,0],
           [1,1,1,1,1]]



bon="☐"
mauvais="X"
for i in range(5):
    for j in range(5):
        if matrice[i][j] == 1:
            print(bon,end=" ")
        else :
            print(mauvais,end=" ")
    print("\n")

list = [] # cree une liste pour verifier les indices 
taille = 5 # taille de la matrice

listIndiceLigne = {} #dictionnaire vide pour acceuillir les indices de lignes
listIndiceCol = {} #dictionnaire vide pour acceuillir les indices de colonnes


# permet de calculer les indices de la matrice donner
def calculIndice(matrice):
    val = 0
    listTmp = []

    listTmp.clear()

    for i in range(taille):

        if matrice[i] == 1:
            val += 1

        elif matrice[i] == 0 and val != 0:
            listTmp.append(val)
            val = 0           

        if i == taille - 1 and val != 0:
            listTmp.append(val)
            val = 0
                
    return listTmp

# parcours pour cree un dictionnaire d'indice de ligne et ajouter les valeurs aux cle 
for i in range(taille):
    
    listIndiceLigne[i] = calculIndice(matrice[i][0:])
    
print("indice de ligne", listIndiceLigne)

# parcours pour creer un dictionnaire d'indice de colonne et ajouter les valeurs aux cle
for j in range(taille):
    colonne = [ligne[j] for ligne in matrice] # renvoie chaque colonne de la matrice
    listIndiceCol[j] = calculIndice(colonne)
print("indice de colonnes", listIndiceCol)

# verifie pour chaque ligne si elle correspond aux indices donner et renvoi true si pareil
def est_valide(matrice, ligne):

    list.clear() 
    n = 0
    for j in range(taille):
        
        # verifie si a l'emplacement il y a un 1 et rajoute a n + 1
        if matrice[j] == 1:
            n += 1
        
        # si ce n'est pas 1 et que n est pas vide alors ajout a la liste et remet n a 0
        elif matrice[j] == 0 and n != 0:
            list.append(n)
            n = 0   

        # si on est a la derniere colonne et que n est pas vide alors on ajoute a la liste
        if j == taille - 1 and n != 0:
            list.append(n)
            n = 0

    # test conditions si la liste et les indices correspondent et renvoie faux ou vrai en fonction
    if ligne != list:
        print(f"La ligne {matrice} n'est pas valide. Attendu : {ligne} - Trouvé : {list}")
        return False
    else:
        print(f"La ligne {matrice} est valide. Attendu : {ligne} - Trouvé : {list}")
        return True


est_valide(matrice[0][0:], listIndiceLigne[0])

# tableau pour afficher
tabAff = [[mauvais for i in range(taille)] for i in range(taille)]


def afficheTab(tabAff):
    for i in range(taille):
        for j in range(taille):
            print(f"{tabAff[i][j]:^4}", end=" ")
        print()


def parcoursPlein():
    for i in range(taille):
        if listIndiceLigne[i] == [5]:
            for k in range(taille):
                tabAff[i][k] = bon
        if listIndiceCol[i] == [5]:
            for j in range(taille):
                tabAff[j][i] = bon
                
parcoursPlein()
afficheTab(tabAff)

