from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# On se place dans un système lame d'air avec un miroir parfait et un autre avec des discontinuités. La lumière émise est monochromatique de longueur d'onde lambda
# On fixe un écran à distance D d'une lentille convergente de focale f, tq f != D car sinon tous les rayons lumineux convergent en un même point

f = 0.5 #en m Focale de la lentille
D = 0.45 #en m Distance écran lentille
wavelength = 520 #en m Longueur d'onde de la source
L = 0.5 #en m Dimension du miroir
I0 = 1

### Fonctions mathématiques utiles

def Heaviside(x):
    if x>0:
        return 1
    else:
        return 0

### Fonctions pour le calcul des différences de marche

def Miroir_echelon():
    global Ndef,dx,dz
    Ndef = 100 #Nombre de défault sur le miroir
    dx = L/Ndef
    dz = 0.001 #en m taille caractéristique d'un défault
    def optic_path(x,y):
        z = 0 #Distance traversé par un rayon lumineux rencontrant un défault
        for i in range(1,Ndef):
            z += Heaviside(abs(x)-i*dx)*dz
        return 2*z
    return optic_path

def Miroir_gauss():
    global dz
    dz = 0.01 #en m hauteur max du défault
    def optic_path(x,y):
        return dz*np.exp(-x**2-y**2)
    return optic_path

def Miroir_sin():
    global dz
    dz = 0.01
    def optic_path(x,y):
        return dz*np.sin(x+y)
    return optic_path

def Miroir_cos():
    global dz
    dz = 0.01
    def optic_path(x,y):
        return dz*np.cos(x+y)
    return optic_path

def Miroir_sinc():
    global dz
    dz = 0.01
    def optic_path(x,y):
        r = np.sqrt(x**2 + y**2)
        return dz*np.sinc(r/(L/2))  # Utilisation de la fonction sinc normalisée
    return optic_path

def Intensite(xp, yp, optic_path):
    """
    Calcule l'intensité lumineuse de deux rayons lumineux dans un interféromètre de Michelson avec un miroir déformé.

    La différence de marche est calculée en fonction de la position (xp, yp) sur le miroir déformé.
    """
    x = xp*f/(f-D)
    y = yp*f/(f-D)
    if abs(x) <= L/2 and abs(y) <= L/2:
        return 2*I0*(1+np.cos(2*np.pi*optic_path(x,y)/(wavelength*1e-9)))
    else:
        return 0

### Affichage

optic_path = Miroir_sinc() #On définie la déformation étudiée
n,m = 1000,1000
X = np.linspace(-L/2,L/2,n)*(f-D)/f #Discrétise le miroir
Y = np.linspace(-L/2,L/2,m)*(f-D)/f

Mat_I = np.zeros((n,m))
for i in range(n):
    xp = X[i]
    for j in range(m):
        yp = Y[j]
        Mat_I[j,i] = Intensite(xp,yp, optic_path)

def wavelength_to_rgb(wavelength):
    """
    Convertit une longueur d'onde (en nm) à une couleur RGB approximative.
    
    Paramètre:
        wavelength (float): Longueur d'onde en nanomètres (nm), entre 380 et 780 nm.
    
    Retour:
        (r, g, b) : Tuple avec les valeurs RGB (compris entre 0 et 1).
    """
    if wavelength >= 380 and wavelength < 440:
        r = -(wavelength - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif wavelength >= 440 and wavelength < 490:
        r = 0.0
        g = (wavelength - 440) / (490 - 440)
        b = 1.0
    elif wavelength >= 490 and wavelength < 510:
        r = 0.0
        g = 1.0
        b = -(wavelength - 510) / (510 - 490)
    elif wavelength >= 510 and wavelength < 580:
        r = (wavelength - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif wavelength >= 580 and wavelength < 645:
        r = 1.0
        g = -(wavelength - 645) / (645 - 580)
        b = 0.0
    elif wavelength >= 645 and wavelength <= 780:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        r = g = b = 0.0  # En dehors du spectre visible

    # Ajuster l'intensité pour tenir compte de la sensibilité de l'œil humain
    if wavelength >= 380 and wavelength < 420:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif wavelength >= 420 and wavelength < 645:
        attenuation = 1.0
    elif wavelength >= 645 and wavelength <= 780:
        attenuation = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)
    else:
        attenuation = 0.0

    r = r * attenuation
    g = g * attenuation
    b = b * attenuation

    return (int(r * 255), int(g * 255), int(b * 255))

# Exemple d'utilisation pour 540 nm
rgb_color = wavelength_to_rgb(wavelength)
hex_color = "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])

def afficher_colormap(array, X, Y, couleur_max, title="Figure d'interférences"):
    """
    Affiche une colormap pour un array 2D (n * m) de flottants avec des labels X et Y,
    où la couleur du maximum est personnalisée et le minimum est noir.
    
    Parameters:
        array (ndarray): Tableau 2D (n * m) contenant des valeurs flottantes.
        X (list or ndarray): Liste des valeurs pour l'axe des abscisses.
        Y (list or ndarray): Liste des valeurs pour l'axe des ordonnées.
        couleur_max (str): La couleur choisie pour la valeur maximale de la colormap (e.g., 'red', 'blue', etc.).
        title (str): Titre de l'affichage (optionnel).
    """
    # Création de la colormap personnalisée allant de noir à la couleur choisie
    cmap_custom = LinearSegmentedColormap.from_list("custom_cmap", ["black", couleur_max])

    plt.figure(figsize=(6, 6))
    
    # Calcul des limites des axes en fonction des valeurs de X et Y
    extent = [min(X), max(X), min(Y), max(Y)]
    
    # Afficher le tableau avec la colormap personnalisée et ajuster les axes
    plt.imshow(array, cmap=cmap_custom, aspect='auto', extent=extent, origin='lower')
    
    # Ajouter une barre de couleur à droite pour la légende
    cbar = plt.colorbar(label="Intensité", orientation='vertical', fraction=0.046, pad=0.04)
    cbar.ax.yaxis.label.set_fontsize(14)

    # Ajouter des labels sur les axes
    plt.xlabel("x (en m)", fontsize = 14)
    plt.ylabel("y (en m)", fontsize = 14)
    
    # Ajouter un titre
    plt.title(title, fontsize = 16)
    
    # Afficher la figure
    plt.show()

afficher_colormap(Mat_I,X,Y,hex_color)