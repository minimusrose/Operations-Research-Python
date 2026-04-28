# PROBLÈME DU SAC À DOS
# Objectif : maximiser la valeur des objets choisis
# Contrainte : ne pas dépasser le poids limite
# Outil : PuLP (programmation linéaire en Python)
# Date : mardi 28 avril 2026

from pulp import *

# Objets : (nom, valeur en €, poids en kg )
objets = [
    ("ordinateur", 500, 3),
    ("telephone", 400, 1),
    ("montre", 300, 1),
    ("livre", 150, 2),
    ("bouteille", 50, 1),
    ("tablette", 350, 2),
]

capacite_max = 4

# Créer le problème : on veut maximiser
prob = LpProblem("sac_a_dos", LpMaximize)

# Variable de décision : prend-on l'objet? 1 = oui, 0 = non
x = {nom: LpVariable(nom, cat = "Binary") for nom, v, p, in objets}


# Maximiser la valeur totale des objets choisis
prob += lpSum(v * x[nom] for nom, v, p in objets)

# Ne pas dépasser la capacité du sac
prob += lpSum(p * x[nom] for nom, v, p in objets) <= capacite_max

# Résolution +  affichage

prob.solve(PULP_CBC_CMD(msg = 0))

print(f"Valeur totale optimale : {value(prob.objective)} €")
print("\nObjets sélectionnés : ")
for nom, v, p in objets : 
    if value(x[nom]) == 1 : 
        print(f" {nom} - {v}€ - {p}kg")