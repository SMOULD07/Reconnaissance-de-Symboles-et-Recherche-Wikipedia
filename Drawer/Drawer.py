from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
import cv2
import numpy as np
from sklearn.neural_network import MLPClassifier

# Dimensions du canvas
width = 200  # Largeur du canvas
height = 200  # Hauteur du canvas
white = (255, 255, 255)  # Couleur de fond

# Fonction pour sauvegarder l'image et la matrice
def save():
    global draw
    # Récupérer le nom de l'image à partir de l'entrée utilisateur
    currentInputText = e1.get()
    filename = currentInputText + ".png"  # Nom du fichier image
    text_filename = currentInputText + ".txt"  # Nom du fichier texte

    # Sauvegarder l'image dessinée
    output_image.save(filename)
    im = cv2.imread(filename)

    # Convertir l'image en niveaux de gris, puis en binaire
    grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY)
    image = image_resize(blackAndWhiteImage, height=20)

    # Sauvegarder l'image réduite
    cv2.imwrite(filename, image)

    # Conversion de l'image en valeurs binaires (0 et 1)
    image[image < 254] = 1
    image[image > 254] = 0

    # Effacer le canvas pour un nouveau dessin
    draw.rectangle((0, 0, width, height), fill="white")
    canvas.delete("all")

    # Afficher la matrice dans le terminal
    print(image)

    # Sauvegarder la matrice dans un fichier texte
    np.savetxt(text_filename, image, fmt='%d')  # Sauvegarde au format entier
    print(f"Matrice enregistrée dans le fichier : {text_filename}")

# Fonction pour redimensionner l'image
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

# Fonction pour dessiner sur le canvas
def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", width=35)
    draw.line([x1, y1, x2, y2], fill="black", width=5)

# Initialisation de l'interface graphique
master = Tk()

# Création du canvas pour dessiner
canvas = Canvas(master, width=width, height=height, bg='white')
canvas.pack()

# Création d'une image PIL vide et d'un objet Draw
output_image = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(output_image)
canvas.pack(expand=YES, fill=BOTH)
canvas.bind("<B1-Motion>", paint)

# Ajout d'un bouton pour sauvegarder l'image
button = Button(text="Save", command=save)
button.pack()

# Zone de saisie pour le nom du fichier
e1 = Entry(master)
e1.pack()

# Lancement de la boucle principale
master.mainloop()
