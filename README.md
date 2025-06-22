# Simulation d’interférences dans une lame d’air déformée

Ce projet simule et visualise la figure d’interférences obtenue dans un montage de type Michelson, où l’un des miroirs présente des défauts (déformations). Le code calcule l’intensité lumineuse résultant de la superposition de deux ondes, en tenant compte de la différence de marche induite par la déformation du miroir.

## Principe

- **Montage** : Un interféromètre de Michelson avec une source monochromatique éclaire une lame d’air. Un miroir est parfait, l’autre présente des défauts (échelon, gaussien, sinusoïdal).
- **Calcul** : Pour chaque point de l’écran, le code calcule la différence de marche optique due à la déformation du miroir, puis l’intensité résultante par interférence.
- **Affichage** : La figure d’interférences est affichée sous forme de colormap, la couleur maximale correspondant à la longueur d’onde choisie.

## Utilisation

1. Exécute `lamedair.py` pour générer et afficher la figure d’interférences.
2. Tu peux modifier la forme du miroir déformé en changeant la fonction utilisée (`Miroir_echelon`, `Miroir_gauss`, `Miroir_sin`).

## Exemple de résultat

<img src="inter_sin.png" alt="Exemple de fractale" width="300"/>
<img src="inter_gauss.png" alt="Exemple de fractale" width="300"/>


## Dépendances

- Python 3
- numpy
- matplotlib

## Auteur

BATAILLE Ewan