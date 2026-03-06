ligne = {0:[4], 1:[1,1], 2:[5], 3:[2], 4:[2,1]}
col = {0:[0], 1:[0], 2:[0], 3:[0], 4:[0]}

matrice = [[1,1,1,1,0],
           [0,1,0,1,0],
           [1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,0,0,1]]



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


est_valide(matrice[0][0:], ligne[0])

#tableau pour afficher
tabAff = [[mauvais for i in range(taille)] for i in range(taille)]


def afficheTab(tabAff):
    for i in range(taille):
        for j in range(taille):
            print(f"{tabAff[i][j]:^4}", end=" ")
        print()

#afficheTab(tabAff)

def parcoursRangeePleine(matrice):
    list.clear() 
    n = 0
    for i in range(taille):
        for j in range(taille):
            # verifie si a l'emplacement il y a un 1 et rajoute a n + 1
            if matrice[i][j] == 1:
                n += 1
            # si on est a la derniere colonne et que n est pas egale a 5 alors on reinitialise
            if j == taille - 1 and n != 5:
                n = 0
            
            # si on est a la derniere colonne et que n vaut 5 alors on peint toutes les cases precedentes et on reinitialise
            elif j == taille - 1 and n == 5:
                n = 0
                for k in range(5):
                    tabAff[i][j - k] = bon
                
            

parcoursRangeePleine(matrice)
afficheTab(tabAff)