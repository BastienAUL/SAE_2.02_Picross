matrice = [
    [1,0,0,0,0],
    [0,1,0,1,0],
    [0,0,1,1,1],
    [0,1,0,0,1],
    [0,1,0,0,0],   
]


bon="☐"
mauvais="X"
inconnu = -1



list = [] # cree une liste pour verifier les indices 
taille = 5 # taille de la matrice





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
def creerIndiceLigne():

    listIndiceLigne = {} #dictionnaire vide pour acceuillir les indices de lignes

    for i in range(taille):
        listIndiceLigne[i] = calculIndice(matrice[i][0:])
    return listIndiceLigne
    

# parcours pour creer un dictionnaire d'indice de colonne et ajouter les valeurs aux cle
def creerIndiceCol():

    listIndiceCol = {} #dictionnaire vide pour acceuillir les indices de colonnes

    for j in range(taille):
        colonne = [ligne[j] for ligne in matrice] # renvoie chaque colonne de la matrice
        listIndiceCol[j] = calculIndice(colonne)
    
    return listIndiceCol


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


# fonction pour afficher la matrice resultat
def afficheTab(tabAff):
    for i in range(taille):
        for j in range(taille):
            print(f"{tabAff[i][j]:^4}", end=" ")
        print()


# genere toute les possibilité pour une ligne ou une colonne donné 
def genererAll(lenght, indice):
    
    if not indice:
        return [[mauvais] * lenght]

    resultat = []
    prem = indice[0]
    rest = indice[1:]

    minCaseUtile = sum(indice) + (len(indice) - 1)
    
    nbDecal = lenght - minCaseUtile
    
    for deb in range(nbDecal + 1):
        premCase = [mauvais] * deb + [bon] * prem
        
        if rest:
            premCase.append(mauvais)
    
        nvLen = lenght - len(premCase)

        for suite in genererAll(nvLen, rest):
            resultat.append(premCase + suite)
            
    return resultat

# met les cases si elles se chevauche que ce soit bon ou pas
def intersection(possibilite):
    
    resultat = []

    for i in range(taille):
        val = [ligne[i] for ligne in possibilite]
        
        if all(c == bon for c in val):
            resultat.append(bon)
        elif all(c == mauvais for c in val):
            resultat.append(mauvais)
        else:
            resultat.append(inconnu)
    return resultat

# filtre les possibilité car certaine sont impossible
def filtrePoss(possibilite, ligne):

    res = []

    for p in possibilite:
        
        ok = True

        for i in range(taille):
            if ligne[i] != inconnu and ligne[i] != p[i]:
                ok = False
                break
        
        if ok:
            res.append(p)
    
    return res


def traiterLigne(tab, possibilite):

    for i in range(taille):

        possVraiLine = filtrePoss(possibilite[i], tab[i])

        deduction = intersection(possVraiLine)

        for j in range(taille):
            if tab[i][j] == inconnu and deduction[j] != inconnu:
                tab[i][j] = deduction[j]

def traiterColonne(tab, possibilite):

    for j in range(taille):

        colonne = [tab[i][j] for i in range(taille)]
            
        possVraiCol = filtrePoss(possibilite[j], colonne)

        deduction = intersection(possVraiCol)

        for i in range(taille):
            if tab[i][j] == inconnu and deduction[i] != inconnu:
                tab[i][j] = deduction[i]

           

            
# propagation sur les lignes et les colonnes 
def propagation(possLine, possCol, taille):
    tabRes = [[inconnu for i in range(taille)] for _ in range(taille)]

    change = True

    while change != False:
        compare = [ligne[:] for ligne in tabRes]

        traiterLigne(tabRes, possLine)
        traiterColonne(tabRes, possCol)

        if compare != tabRes:
            change = True
        else:
            change = False

    return tabRes

# verifie si la grille est complete
def grilleComplete(tab):
    res = True
    for ligne in tab:
        if inconnu in ligne:
            res = False
    return res

# renvoie la position d'une case inconnue
def trouverCaseInconnue(tab):
    for i in range(taille):
        for j in range(taille):

            if tab[i][j] == inconnu:
              return(i, j)
    return None


# backtracking pour les cases inconnus
def backtracking(tab, possLine, possCol):

    if grilleComplete(tab):
        return True

    case = trouverCaseInconnue(tab)

    if case == None:
        return True

    i, j = case

    for val in [bon, mauvais]:

        tabRes = [ligne[:] for ligne in tab]
        tabRes[i][j] = val

        if backtracking(tabRes, possLine, possCol):

            for k in range(taille):
                tab[k] = tabRes[k][:]
            return True
    
    return False

def main():
    indiceLigne = creerIndiceLigne()
    listIndiceLigne = [indiceLigne[i] for i in sorted(indiceLigne.keys())]

    indiceCol = creerIndiceCol()
    listIndiceCol = [indiceCol[i] for i in sorted(indiceCol.keys())]

    possLine = [genererAll(taille, indice) for indice in listIndiceLigne]
    possCol = [genererAll(taille, indice) for indice in listIndiceCol]

    tabAff = propagation(possLine, possCol, taille)

    res = backtracking(tabAff, possLine, possCol)

    if res == True:
        afficheTab(tabAff)
    else:
        print("pas de solution")

main()