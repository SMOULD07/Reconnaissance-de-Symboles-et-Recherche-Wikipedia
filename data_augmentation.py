import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

# Dossier contenant vos classes
input_folder = './'  # Chemin racine des dossiers (lettre_a, lettre_b, etc.)
image_size = (20, 20)  # Taille cible des images
augmentations_per_image = 5  # Nombre d'augmentations par image

# Fonction pour charger une image à partir d'un fichier .txt
def load_image_from_txt(file_path):
    matrix = np.loadtxt(file_path, dtype=int)  # Charger la matrice depuis le fichier .txt
    return cv2.resize(matrix, image_size)  # Redimensionner l'image

# Appliquer la data augmentation
def augment_data():
    datagen = ImageDataGenerator(
        rotation_range=15,       # Rotation aléatoire entre -15° et 15°
        width_shift_range=0.1,   # Décalage horizontal aléatoire
        height_shift_range=0.1,  # Décalage vertical aléatoire
        shear_range=0.1,         # Cisaillement aléatoire
        zoom_range=0.1,          # Zoom avant/arrière
        fill_mode='nearest'      # Remplissage pour les zones manquantes
    )

    # Parcourir chaque sous-dossier (classe)
    for class_name in os.listdir(input_folder):
        class_path = os.path.join(input_folder, class_name)
        if not os.path.isdir(class_path):  # Vérifier si c'est un dossier
            continue

        print(f"Traitement de la classe : {class_name}")

        # Parcourir les fichiers .txt de la classe
        for file_name in os.listdir(class_path):
            if file_name.endswith('.txt'):  # Ne traiter que les fichiers .txt
                file_path = os.path.join(class_path, file_name)

                # Charger l'image à partir du fichier .txt
                image = load_image_from_txt(file_path)

                # Normaliser l'image entre 0 et 1
                image = image / 255.0
                image = image.reshape((1, image_size[0], image_size[1], 1))  # Ajouter les dimensions batch et canal

                # Générer des augmentations
                i = 0
                for batch in datagen.flow(image, batch_size=1):
                    augmented_image = batch[0].reshape(image_size)  # Retirer les dimensions batch et canal

                    # Sauvegarder l'image augmentée sous forme de fichier .txt
                    output_file_name = f"{os.path.splitext(file_name)[0]}_aug{i}.txt"
                    output_file_path = os.path.join(class_path, output_file_name)
                    np.savetxt(output_file_path, (augmented_image * 255).astype(int), fmt='%d')

                    i += 1
                    if i >= augmentations_per_image:
                        break  # Générer uniquement le nombre souhaité d'augmentations

    print("Data augmentation terminée.")

# Exécuter la data augmentation
augment_data()
