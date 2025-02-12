from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
import cv2
import numpy as np
import joblib
import wikipedia

# Charger le modèle MLP entraîné
model = joblib.load('mlp_symbol_recognition.pkl')  # Assurez-vous que ce fichier est dans le même dossier

# Définir les classes (assurez-vous qu'elles correspondent au modèle entraîné)
classes = ['lettre_a', 'lettre_b', 'lettre_c', 'lettre_y']

# Dimensions du canvas
width = 200  # Largeur du canvas
height = 200  # Hauteur du canvas
white = (255, 255, 255)  # Couleur de fond

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

# Fonction pour sauvegarder l'image dessinée et générer une matrice binaire 20x20
def save(draw, canvas):
    # Sauvegarder l'image dessinée temporairement
    output_image.save("temp_image.png")
    im = cv2.imread("temp_image.png")

    # Convertir l'image en niveaux de gris, puis en binaire
    grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY)
    image = image_resize(blackAndWhiteImage, height=20)

    # Sauvegarder l'image réduite
    cv2.imwrite("temp_image.png", image)

    # Conversion de l'image en valeurs binaires (0 et 1)
    image[image < 254] = 1
    image[image > 254] = 0

    # Effacer le canvas pour un nouveau dessin
    draw.rectangle((0, 0, width, height), fill="white")
    canvas.delete("all")

    # Sauvegarder la matrice dans un fichier texte
    np.savetxt("temp_image.txt", image, fmt='%d')  # Sauvegarde au format entier
    return image

# Fonction pour récupérer les détails d'une page Wikipedia
def fetch_page_details(keyword, language='fr'):
    wikipedia.set_lang(language)
    try:
        # Recherche des pages correspondant au mot-clé
        search_results = wikipedia.search(keyword)
        if not search_results:
            return {"error": "Aucun résultat trouvé pour ce mot-clé."}
        # Récupérer la première page trouvée
        first_page_title = search_results[0]
        page = wikipedia.page(first_page_title)  # Rassembler les informations
        return {
            "title": first_page_title,
            "content": page.content,
            "internal_links": page.links,
            "external_links": page.references
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {"error": f"Ambiguïté détectée. Plusieurs options : {e.options}"}
    except wikipedia.exceptions.PageError:
        return {"error": "La page demandée n'existe pas."}
    except Exception as e:
        return {"error": f"Une erreur s'est produite : {e}"}

# Fonction pour prédire la lettre dessinée et effectuer une requête Wikipedia
def predict():
    # Appeler la fonction save pour obtenir la matrice binaire
    binary_image = save(draw, canvas)

    # Afficher la matrice binaire dans le terminal
    print("Matrice binaire utilisée pour la prédiction (20x20) :")
    print(binary_image)

    # Aplatir la matrice pour la prédiction
    flattened_image = binary_image.flatten()

    # Faire la prédiction
    prediction = model.predict([flattened_image])
    predicted_class = classes[prediction[0]]

    # Afficher le résultat
    print(f"Prédiction : {predicted_class}")
    result_label.config(text=f"Prédiction : {predicted_class}")

    # Requête Wikipedia
    details = fetch_page_details(predicted_class)

    if "error" in details:
        wikipedia_label.config(text=details["error"])
    else:
        # Synthétiser le contenu pour l'affichage
        content_preview = details["content"][:500] + "..." if len(details["content"]) > 500 else details["content"]
        wikipedia_label.config(
            text=f"Résumé de Wikipedia :\n{content_preview}\n\nPlus d'informations : {details['title']}"
        )

# Fonction pour dessiner sur le canvas
def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", width=35)
    draw.line([x1, y1, x2, y2], fill="black", width=5)

# Initialisation de l'interface graphique
master = Tk()
master.title("Reconnaissance de lettres - Prédiction avec Wikipedia")

# Création du canvas pour dessiner
canvas = Canvas(master, width=width, height=height, bg='white')
canvas.pack()

# Création d'une image PIL vide et d'un objet Draw
output_image = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(output_image)
canvas.pack(expand=YES, fill=BOTH)
canvas.bind("<B1-Motion>", paint)

# Bouton pour prédire
button = Button(text="Prédire", command=predict)
button.pack()

# Label pour afficher le résultat
result_label = Label(master, text="Dessinez une lettre et cliquez sur Prédire")
result_label.pack()

# Label pour afficher les informations Wikipedia
wikipedia_label = Label(master, text="Résumé de Wikipedia apparaîtra ici.", wraplength=400, justify=LEFT)
wikipedia_label.pack()

# Lancement de la boucle principale
master.mainloop()
