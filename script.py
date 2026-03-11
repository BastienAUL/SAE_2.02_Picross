ligne = {0:[1,2], 1:[1,1], 2:[5], 3:[2], 4:[1,1,1]}
col = {0:[1,1,1], 1:[3], 2:[1,3], 3:[3], 4:[1,1]}

"""matrice = [[1,0,1,1,0],
           [0,1,0,1,0],
           [1,1,1,1,1],
           [0,1,1,0,0],
           [1,0,1,0,1]]"""

matrice = [[0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0]]

bon="☐"
mauvais=" "
for i in range(5):
    for j in range(5):
        if matrice[i][j] == 1:
            print(bon,end=" ")
        else :
            print(mauvais,end=" ")
    print("\n")

trouveligne = [[],[],[],[],[]]
trouvecol = [[],[],[],[],[]]
trouvecol2 = [[],[],[],[],[]]

listligne = []
listcol = []

def trouvematrice(ligne,col):
    for k, v in ligne.items():
        for n in v:
            for i in range(n):
                trouveligne[k].append(1)
            if len(trouveligne[k]) < 5:
                trouveligne[k].append(0)
        while len(trouveligne[k]) < 5:
            trouveligne[k].append(0)
    print(trouveligne,"\n")
    for k, v in col.items():
        for n in v:
            for i in range(n):
                trouvecol[k].append(1)
            if len(trouvecol[k]) < 5:
                trouvecol[k].append(0)
        while len(trouvecol[k]) < 5:
            trouvecol[k].append(0)
    for i in range(5):
        for j in range(5):
            if trouvecol[j][i] == 1:
                trouvecol2[i].append(1)
            else:
                trouvecol2[i].append(0)
    for i in range(5):
         print (trouveligne[i],"\n")
    print("\n")
    for i in range(5):
         print (trouvecol2[i],"\n")

def win():
    valide = True
    for i in range(5):
        listligne.clear()
        n=0
        for j in range(5):
            indice = matrice[i][j]
            if indice == 1:
                n += 1
            elif indice == 0 and n != 0:
                listligne.append(n)
                n = 0
            if j == 4 and n!= 0:
                    listligne.append(n)
                    n = 0
        if ligne[i] != listligne:
                print(f"La ligne {i+1} n'est pas valide. Attendu : {ligne[i]} - Trouvé : {listligne}")
                valide = False
        else:
                print(f"La ligne {i+1} est valide. Attendu : {ligne[i]} - Trouvé : {listligne}")
    for j in range(5):
        listcol.clear()
        n=0
        for i in range(5):
            indice = matrice[i][j]
            if indice == 1:
                n += 1
            elif indice == 0 and n != 0:
                listcol.append(n)
                n = 0
            if i == 4 and n!= 0:
                    listcol.append(n)
                    n = 0
        if col[j] != listcol:
                print(f"La colonne {j+1} n'est pas valide. Attendu : {col[j]} - Trouvé : {listcol}")
                valide = False
        else:
                print(f"La colonne {j+1} est valide. Attendu : {col[j]} - Trouvé : {listcol}")
    if valide:
        print("La réponse trouvé est correct est valide.")
    else:        
        print("La matrice n'est pas valide.")
        
trouvematrice(ligne,col)