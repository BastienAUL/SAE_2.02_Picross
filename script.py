ligne = {0:[1,2], 1:[1,1], 2:[5], 3:[2], 4:[1,1,1]}
col = {0:[0], 1:[0], 2:[0], 3:[0], 4:[0]}

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

list = []

def est_valide():
    for i in range(5):
        list.clear()
        n=0
        for j in range(5):
            indice = matrice[i][j]
            if indice == 1:
                n += 1
            elif indice == 0 and n != 0:
                list.append(n)
                n = 0
            elif j == 4 and n!= 0:
                    list.append(n)
                    n = 0
        if ligne[i] != list:
                print(f"La ligne {i+1} n'est pas valide. Attendu : {ligne[i]} - Trouvé : {list}")
        else:
                print(f"La ligne {i+1} est valide. Attendu : {ligne[i]} - Trouvé : {list}")

est_valide()
