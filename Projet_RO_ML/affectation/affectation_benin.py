# Problème d'affectation -Enseignants et lycée
# Auteur : Marie-Odette | Master 1 RO, IMSP, UAC

import pulp
import matplotlib.pyplot as plt
import numpy as np

# Les agents et les tâches

enseignants = ["Aicha", "Brice", "Céleste", "Darius"]
etablissements = ["Lycée Coulibaly", "CEG Akpakpa", "Lycée Béhanzin", "CEG Cadjèhoun" ]

# Matrice des coûts (en FCFA de transport/ semaine)

couts = {
    "Aicha" : {
        "Lycée Coulibaly" : 8000,
        "CEG Akpakpa" : 5000,
        "Lycée Béhanzin" : 9000, 
        "CEG Cadjèhoun" : 3000
    },
    "Brice" : {
        "Lycée Coulibaly" : 6000,
        "CEG Akpakpa" : 4000,
        "Lycée Béhanzin" : 7000, 
        "CEG Cadjèhoun" : 8000
    },
    "Céleste" : {
        "Lycée Coulibaly" : 9000,
        "CEG Akpakpa" : 11000,
        "Lycée Béhanzin" : 4000, 
        "CEG Cadjèhoun" : 6000
    },
    "Darius" : {
        "Lycée Coulibaly" : 7000,
        "CEG Akpakpa" : 6000,
        "Lycée Béhanzin" : 5000, 
        "CEG Cadjèhoun" : 9000
    }
}

# Vérification rapide

print(f"{len(enseignants)} enseignants, {len(etablissements)} établissements")
couts_def = 0
for enseignant in enseignants : 
    couts_def +=len(couts[enseignant])

print(f"{couts_def} coûts définis - attendus : {len(enseignants)*len(etablissements)}")


# Création du modèle
prob = pulp.LpProblem("Affectation_Benin", pulp.LpMinimize)

# Variables de décision : x[i][j] = 1 si enseignant i affecté à l'établissement j

x = {
    i : {
        j: pulp.LpVariable(f"x_{i}_{j}", cat = "Binary")
        for j in etablissements
    }
    for i in enseignants
}

# Vérification
print(f"Exemple : {x["Aicha"]['CEG Akpakpa']}")

# Fontion objectif : minimiser le coût total 
prob += pulp.lpSum(couts[i][j]*x[i][j] for i in enseignants for j in etablissements), "Coût_total"

print("\nFonction objectif ajoutée")
print(prob, "=", prob.objective)

# Contraintes
# A Chaque enseignant est affecté un seul établissement
for i in enseignants : 
    prob += pulp.lpSum(x[i][j] for j in etablissements) == 1, f"Enseignant_{i}"

# Chaque etablissement reçoit exactement un enseignant

for j in etablissements : 
    prob += pulp.lpSum(x[i][j] for i in enseignants) == 1, f"Etablissement_{j}"

# Vérification
print(f"Nombre de contraintes : {len(prob.constraints)}")
print("\nListe des contraintes : ")
for nom, contrainte in prob.constraints.items() : 
    print(f" {nom} : {contrainte}")

# Résolution du problème
prob.solve(pulp.PULP_CBC_CMD(msg = 0))

#Statut
print(f"Statut : {pulp.LpStatus[prob.status]}")
print(f"Coût optimal : {pulp.value(prob.objective):,.0f} FCFA\n")

# Affichage de la solution
print("Affectation optimale : ")
for i in enseignants : 
    for j in etablissements : 
        if pulp.value(x[i][j])==1 : 
            print(f" {i} -> {j} : {couts[i][j] :,} FCFA")



# Visualisation
fig, ax1 = plt.subplots(figsize = (8, 5))
fig.suptitle("Problème d'affectation - Enseignants & Lycées, Cotonou", fontsize = 13, fontweight = 'bold')

# Heatmap de la matrice des coûts
ax1.set_title("Matrice des coûts (FCFA)", fontsize = 11)

matrice = np.array([[couts[i][j] for j in etablissements] 
  for i in enseignants                 
])

im = ax1.imshow(matrice, cmap = "YlOrRd")
ax1.set_xticks(range(len(etablissements)))
ax1.set_yticks(range(len(enseignants)))
ax1.set_xticklabels(etablissements, rotation = 20, ha = 'right', fontsize = 9)
ax1.set_yticklabels(enseignants, fontsize=9)

for i in range(len(enseignants)) : 
    for j in range(len(etablissements)) : 
        ax1.text(j, i, f"{matrice[i, j]:,}", ha = "center", va = "center", fontsize = 9)

for i, ens in enumerate(enseignants) : 
    for j, etab in enumerate(etablissements) : 
        if pulp.value(x[ens][etab]) == 1 : 
            ax1.add_patch(plt.Rectangle(
                (j - 0.5, i - 0.5), 1, 1, fill = False, edgecolor = 'blue', lw = 3

))
            
plt.colorbar(im, ax = ax1)
plt.tight_layout()
plt.savefig("affectation_benin.png", dpi = 150, bbox_inches = 'tight')
plt.show()
print("Graphique sauvegardé → affectation_benin.png")
