def calcul_indices_ligne(sequence):
    compteur = 0
    resultat = []

    for case in sequence:
        if case == 1:
            compteur += 1
        elif compteur:
            resultat.append(compteur)
            compteur = 0

    if compteur:
        resultat.append(compteur)

    return resultat


def calcul_indices_lignes(matrice_source):
    return [calcul_indices_ligne(ligne) for ligne in matrice_source]


def calcul_indices_colonnes(matrice_source):
    if not matrice_source:
        return []

    taille_locale = len(matrice_source)
    indices_colonnes = []

    for colonne in range(taille_locale):
        valeurs_colonne = [matrice_source[ligne][colonne] for ligne in range(taille_locale)]
        indices_colonnes.append(calcul_indices_ligne(valeurs_colonne))

    return indices_colonnes


def resoudre_depuis_indices(indices_lignes, indices_colonnes):
    if not indices_lignes or not indices_colonnes:
        return False, [], False

    taille_locale = len(indices_lignes)
    if len(indices_colonnes) != taille_locale:
        return False, [[-1 for _ in range(taille_locale)] for _ in range(taille_locale)], False

    def generer_toutes_possibilites(longueur, indices):
        if not indices:
            return [[0] * longueur]

        resultat = []
        premier = indices[0]
        reste = indices[1:]
        minimum = sum(indices) + (len(indices) - 1)
        decalages = longueur - minimum

        if decalages < 0:
            return []

        for debut in range(decalages + 1):
            prefixe = [0] * debut + [1] * premier
            if reste:
                prefixe.append(0)

            nouvelle_longueur = longueur - len(prefixe)
            for suite in generer_toutes_possibilites(nouvelle_longueur, reste):
                resultat.append(prefixe + suite)

        return resultat

    def filtrer_possibilites(possibilites, ligne_actuelle):
        resultat = []

        for candidat in possibilites:
            valide = True
            for i in range(taille_locale):
                if ligne_actuelle[i] != -1 and ligne_actuelle[i] != candidat[i]:
                    valide = False
                    break
            if valide:
                resultat.append(candidat)

        return resultat

    def intersection(possibilites):
        if not possibilites:
            return [-1] * taille_locale

        resultat = []

        for i in range(taille_locale):
            valeurs = [ligne[i] for ligne in possibilites]
            if all(v == 1 for v in valeurs):
                resultat.append(1)
            elif all(v == 0 for v in valeurs):
                resultat.append(0)
            else:
                resultat.append(-1)

        return resultat

    def propagation(grille, poss_lignes, poss_colonnes):
        changement = True
        while changement:
            changement = False

            for i in range(taille_locale):
                valides = filtrer_possibilites(poss_lignes[i], grille[i])
                deduits = intersection(valides)
                for j in range(taille_locale):
                    if grille[i][j] == -1 and deduits[j] != -1:
                        grille[i][j] = deduits[j]
                        changement = True

            for j in range(taille_locale):
                colonne = [grille[i][j] for i in range(taille_locale)]
                valides = filtrer_possibilites(poss_colonnes[j], colonne)
                deduits = intersection(valides)
                for i in range(taille_locale):
                    if grille[i][j] == -1 and deduits[i] != -1:
                        grille[i][j] = deduits[i]
                        changement = True

    def grille_complete(grille):
        return all(-1 not in ligne for ligne in grille)

    def grille_coherente(grille, poss_lignes, poss_colonnes):
        for i in range(taille_locale):
            if not filtrer_possibilites(poss_lignes[i], grille[i]):
                return False

        for j in range(taille_locale):
            colonne = [grille[i][j] for i in range(taille_locale)]
            if not filtrer_possibilites(poss_colonnes[j], colonne):
                return False

        return True

    def chercher_case_inconnue(grille):
        for i in range(taille_locale):
            for j in range(taille_locale):
                if grille[i][j] == -1:
                    return i, j
        return None

    def compter_solutions(grille, poss_lignes, poss_colonnes, limite=2):
        if grille_complete(grille):
            return [tuple(tuple(case for case in ligne) for ligne in grille)]

        case = chercher_case_inconnue(grille)
        if case is None:
            return [tuple(tuple(case for case in ligne) for ligne in grille)]

        i, j = case
        solutions = []

        for valeur in (1, 0):
            essai = [ligne[:] for ligne in grille]
            essai[i][j] = valeur

            if not grille_coherente(essai, poss_lignes, poss_colonnes):
                continue

            propagation(essai, poss_lignes, poss_colonnes)
            solutions.extend(compter_solutions(essai, poss_lignes, poss_colonnes, limite))

            uniques = []
            deja = set()
            for solution in solutions:
                if solution not in deja:
                    deja.add(solution)
                    uniques.append(solution)
            solutions = uniques

            if len(solutions) >= limite:
                return solutions[:limite]

        return solutions

    poss_lignes = [generer_toutes_possibilites(taille_locale, indices) for indices in indices_lignes]
    poss_colonnes = [generer_toutes_possibilites(taille_locale, indices) for indices in indices_colonnes]

    if any(not possibilites for possibilites in poss_lignes) or any(not possibilites for possibilites in poss_colonnes):
        return False, [[-1 for _ in range(taille_locale)] for _ in range(taille_locale)], False

    grille = [[-1 for _ in range(taille_locale)] for _ in range(taille_locale)]
    propagation(grille, poss_lignes, poss_colonnes)
    solutions = compter_solutions(grille, poss_lignes, poss_colonnes, limite=2)

    if not solutions:
        return False, grille, False

    solution = [[case for case in ligne] for ligne in solutions[0]]
    est_unique = len(solutions) == 1
    return True, solution, est_unique


def _demo_console():
    matrice_demo = [
        [0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1],
    ]

    indices_lignes = calcul_indices_lignes(matrice_demo)
    indices_colonnes = calcul_indices_colonnes(matrice_demo)
    trouve, solution, est_unique = resoudre_depuis_indices(indices_lignes, indices_colonnes)

    print("Indices lignes:", indices_lignes)
    print("Indices colonnes:", indices_colonnes)
    print("Trouve:", trouve)
    print("Unique:", est_unique)
    print("Solution:")
    for ligne in solution:
        print(ligne)


if __name__ == "__main__":
    _demo_console()
