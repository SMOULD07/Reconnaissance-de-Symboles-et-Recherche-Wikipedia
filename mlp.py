import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Paramètres
matrix_size = (20, 20)  # Taille des matrices
classes = ['lettre_a', 'lettre_b', 'lettre_c', 'lettre_y']
data_dir = './'  # Répertoire des fichiers .txt

# Charger les données et binariser les matrices
def load_data():
    X = []
    y = []
    for label, class_name in enumerate(classes):
        folder_path = os.path.join(data_dir, class_name)
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                # Charger la matrice
                matrix = np.loadtxt(file_path, dtype=int)
                # Binariser la matrice
                X.append(matrix.flatten())  # Aplatir la matrice
                y.append(label)
    return np.array(X), np.array(y)

# Charger les données
X, y = load_data()
print(f"Données chargées : {X.shape[0]} exemples.")

# Vérifier l'équilibre des classes
from collections import Counter
print(f"Distribution des classes : {Counter(y)}")

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normaliser les données (binaire, donc inutile ici, mais stable pour le MLP)
X_train = X_train / 1.0
X_test = X_test / 1.0

# Initialiser le modèle MLP
mlp = MLPClassifier(
    hidden_layer_sizes=(512,),
    activation='relu',
    solver='adam',
    max_iter=10,
    random_state=42
)

# Entraîner le modèle
print("Entraînement du modèle...")
mlp.fit(X_train, y_train)

# Évaluer le modèle
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision sur l'ensemble de test : {accuracy * 100:.2f}%")

# Rapport de classification
print("\nRapport de classification :")
print(classification_report(y_test, y_pred, target_names=classes))

# Sauvegarder le modèle
joblib.dump(mlp, 'mlp_symbol_recognition.pkl')
print("Modèle sauvegardé sous 'mlp_symbol_recognition.pkl'")
