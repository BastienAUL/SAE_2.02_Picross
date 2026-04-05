import tkinter as tk
from tkinter import messagebox, ttk

from bastien import calcul_indices_colonnes, calcul_indices_lignes, resoudre_depuis_indices


class PicrossSimpleApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Picross simple")
        self.fenetre.geometry("900x680")

        self.taille_var = tk.IntVar(value=10)
        self.taille = 0
        self.taille_case = 30
        self.grille = []
        self.cadre_depart = ttk.Frame(self.fenetre, padding=24)
        self.cadre_principal = ttk.Frame(self.fenetre, padding=12)
        self.panneau = None
        self.zone_grille = None
        self.cadre_canvas = None
        self.barre_horizontale = None
        self.barre_verticale = None
        self.zone_resultat = None
        self._vue_depart()

    def _texte_matrice(self):
        lignes = []
        for ligne in self.grille:
            lignes.append(" ".join(str(case) for case in ligne))
        return "\n".join(lignes)

    def _redimensionner_fenetre(self):
        largeur_grille = self.taille_case * self.taille
        largeur = max(900, min(1600, largeur_grille + 420))
        hauteur = max(700, min(1100, largeur_grille + 190))
        self.fenetre.minsize(820, 620)
        self.fenetre.geometry(f"{largeur}x{hauteur}")

    def _vue_depart(self):
        self.cadre_principal.pack_forget()
        self.cadre_depart.pack(fill="both", expand=True)
        for enfant in self.cadre_depart.winfo_children():
            enfant.destroy()

        ttk.Label(self.cadre_depart, text="Picross tres simple", font=("Segoe UI", 20, "bold")).pack(pady=(30, 20))
        cadre = ttk.LabelFrame(self.cadre_depart, text="Choix taille", padding=18)
        cadre.pack()
        ttk.Label(cadre, text="Taille de la matrice (NxN):").grid(row=0, column=0, padx=(0, 10), sticky="w")
        ttk.Spinbox(cadre, from_=5, to=25, textvariable=self.taille_var, width=8).grid(row=0, column=1)
        ttk.Button(cadre, text="Creer la grille", command=self._creer_grille).grid(row=1, column=0, columnspan=2, pady=(14, 0))

    def _creer_grille(self):
        taille = self.taille_var.get()
        if taille < 5 or taille > 25:
            messagebox.showerror("Erreur", "La taille doit etre entre 5 et 25.")
            return

        self.taille = taille
        self.grille = [[0 for _ in range(self.taille)] for _ in range(self.taille)]
        self.taille_case = max(20, min(72, 720 // self.taille))
        self._redimensionner_fenetre()
        self.cadre_depart.pack_forget()
        self.cadre_principal.pack(fill="both", expand=True)

        for enfant in self.cadre_principal.winfo_children():
            enfant.destroy()

        barre_haut = ttk.Frame(self.cadre_principal)
        barre_haut.pack(fill="x", pady=(0, 8))
        ttk.Button(barre_haut, text="Changer taille", command=self._vue_depart).pack(side="left", padx=(0, 8))
        ttk.Button(barre_haut, text="Tout effacer", command=self._vider).pack(side="left", padx=(0, 8))
        ttk.Button(barre_haut, text="Calculer indices", command=self._calculer).pack(side="left")
        ttk.Button(barre_haut, text="Resoudre avec indices", command=self._resoudre).pack(side="left", padx=(8, 0))

        self.panneau = ttk.PanedWindow(self.cadre_principal, orient="horizontal")
        self.panneau.pack(fill="both", expand=True)

        cadre_gauche = ttk.LabelFrame(self.panneau, text="Grille", padding=8)
        cadre_droit = ttk.LabelFrame(self.panneau, text="Resultat", padding=8)
        self.panneau.add(cadre_gauche, weight=5)
        self.panneau.add(cadre_droit, weight=2)

        taille_zone = self.taille_case * self.taille

        self.cadre_canvas = ttk.Frame(cadre_gauche)
        self.cadre_canvas.pack(fill="both", expand=True)

        largeur_visible = min(taille_zone, 900)
        hauteur_visible = min(taille_zone, 760)

        self.zone_grille = tk.Canvas(
            self.cadre_canvas,
            width=largeur_visible,
            height=hauteur_visible,
            bg="#f7f7f7",
            highlightthickness=0,
        )
        self.barre_horizontale = ttk.Scrollbar(self.cadre_canvas, orient="horizontal", command=self.zone_grille.xview)
        self.barre_verticale = ttk.Scrollbar(self.cadre_canvas, orient="vertical", command=self.zone_grille.yview)

        self.zone_grille.configure(xscrollcommand=self.barre_horizontale.set, yscrollcommand=self.barre_verticale.set)
        self.zone_grille.grid(row=0, column=0, sticky="nsew")
        self.barre_verticale.grid(row=0, column=1, sticky="ns")
        self.barre_horizontale.grid(row=1, column=0, sticky="ew")

        self.cadre_canvas.grid_rowconfigure(0, weight=1)
        self.cadre_canvas.grid_columnconfigure(0, weight=1)

        self.zone_grille.bind("<Button-1>", self._clic)

        self.zone_resultat = tk.Text(cadre_droit, wrap="word", height=34, width=34)
        self.zone_resultat.pack(fill="both", expand=True)

        self.fenetre.update_idletasks()
        largeur = max(900, self.fenetre.winfo_width())
        self.panneau.sashpos(0, int(largeur * 0.72))

        self._dessiner()

    def _dessiner(self):
        self.zone_grille.delete("all")
        for ligne in range(self.taille):
            for colonne in range(self.taille):
                x1 = colonne * self.taille_case
                y1 = ligne * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
                couleur = "#111111" if self.grille[ligne][colonne] else "#ffffff"
                self.zone_grille.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="#999999")

            taille_zone = self.taille_case * self.taille
            self.zone_grille.configure(scrollregion=(0, 0, taille_zone, taille_zone))

    def _clic(self, evenement):
        colonne = evenement.x // self.taille_case
        ligne = evenement.y // self.taille_case
        if 0 <= ligne < self.taille and 0 <= colonne < self.taille:
            self.grille[ligne][colonne] = 0 if self.grille[ligne][colonne] == 1 else 1
            self._dessiner()

    def _vider(self):
        for ligne in range(self.taille):
            for colonne in range(self.taille):
                self.grille[ligne][colonne] = 0
        self._dessiner()
        self._ecrire("Grille vide.\n")

    def _calculer(self):
        try:
            indices_lignes = calcul_indices_lignes(self.grille)
            indices_colonnes = calcul_indices_colonnes(self.grille)
            lignes_texte = ["Matrice (0/1):", self._texte_matrice(), "", "Indices lignes:"]
            for index_ligne, valeurs in enumerate(indices_lignes):
                lignes_texte.append(f"L{index_ligne + 1}: {valeurs}")
            lignes_texte.append("")
            lignes_texte.append("Indices colonnes:")
            for index_colonne, valeurs in enumerate(indices_colonnes):
                lignes_texte.append(f"C{index_colonne + 1}: {valeurs}")

            print("[Picross] Matrice 0/1:")
            print(self._texte_matrice())
            self._ecrire("\n".join(lignes_texte))
        except Exception as erreur:
            print(f"[Picross] Erreur calcul indices: {erreur}")
            messagebox.showerror("Erreur", f"Erreur calcul indices: {erreur}")

    def _resoudre(self):
        try:
            indices_lignes = calcul_indices_lignes(self.grille)
            indices_colonnes = calcul_indices_colonnes(self.grille)
            trouve, solution, est_unique = resoudre_depuis_indices(indices_lignes, indices_colonnes)

            lignes_texte = ["Matrice (0/1):", self._texte_matrice(), "", "Indices lignes:"]
            for index_ligne, valeurs in enumerate(indices_lignes):
                lignes_texte.append(f"L{index_ligne + 1}: {valeurs}")

            lignes_texte.append("")
            lignes_texte.append("Indices colonnes:")
            for index_colonne, valeurs in enumerate(indices_colonnes):
                lignes_texte.append(f"C{index_colonne + 1}: {valeurs}")

            lignes_texte.append("")
            lignes_texte.append("Solution:")
            for ligne in solution:
                lignes_texte.append(" ".join("#" if case == 1 else "." for case in ligne))

            lignes_texte.append("")
            if trouve:
                lignes_texte.append("Statut: solution trouvee.")
                if est_unique:
                    lignes_texte.append("Unicite: solution unique.")
                    print("[Picross] Solution unique: OUI")
                else:
                    lignes_texte.append("Unicite: plusieurs solutions possibles.")
                    print("[Picross] Solution unique: NON")
            else:
                lignes_texte.append("Statut: impossible de trouver une solution complete.")
                print("[Picross] Solution unique: NON (aucune solution)")

            print("[Picross] Matrice 0/1:")
            print(self._texte_matrice())
            self._ecrire("\n".join(lignes_texte))
        except Exception as erreur:
            print(f"[Picross] Erreur resolution: {erreur}")
            messagebox.showerror("Erreur", f"Erreur resolution: {erreur}")

    def _ecrire(self, texte):
        self.zone_resultat.delete("1.0", tk.END)
        self.zone_resultat.insert(tk.END, texte)


def main():
    fenetre = tk.Tk()
    style = ttk.Style(fenetre)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    PicrossSimpleApp(fenetre)
    fenetre.mainloop()


if __name__ == "__main__":
    main()
