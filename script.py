ligne = {0:[1,2], 1:[1,1], 2:[5], 3:[2], 4:[1,1,1]}
col = {0:[1,1,1], 1:[3], 2:[1,3], 3:[3], 4:[1,1]}

matrice = [[1,0,1,1,0],
           [0,1,0,1,0],
           [1,1,1,1,1],
           [0,1,1,0,0],
           [1,0,1,0,1]]

bon="☐"
mauvais=" "
for i in range(5):
    for j in range(5):
        if matrice[i][j] == 1:
            print(bon,end=" ")
        else :
            print(mauvais,end=" ")
    print("\n")

listligne = []
listcol = []

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

win()
