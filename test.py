ligne = {0:[1,2], 1:[1,1], 2:[5], 3:[2], 4:[2,1]}
col = {0:[0], 1:[0], 2:[0], 3:[0], 4:[0]}

matrice = [[1,0,1,1,0],
           [0,1,0,1,0],
           [1,1,1,1,1],
           [0,1,1,0,0],
           [1,1,0,0,1]]

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

def est_valide(matrice, ligne):
    
    list.clear()
    n = 0
    j = 0
    while j != 4:
        
        if matrice == 1:
            n += 1
        elif matrice == 0 and n != 0:
            list.append(n)
            n = 0
        j += 1
        
    if j == 4 and n != 0:
        list.append(n)
        n = 0
        
    if ligne != list:
        print(f"La ligne {matrice} n'est pas valide. Attendu : {ligne} - Trouvé : {list}")
    else:
        print(f"La ligne {matrice} est valide. Attendu : {ligne} - Trouvé : {list}")

est_valide(matrice[0][0], ligne[0])


#def backtracking():
     