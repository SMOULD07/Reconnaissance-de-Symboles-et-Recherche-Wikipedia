
# Projet de Reconnaissance de Symboles avec Prédiction et Recherche Wikipedia

## 1. Présentation des Scripts

Ce projet inclut une suite de scripts permettant de dessiner des symboles, de les reconnaître grâce à un modèle MLP, et d'afficher des informations issues de Wikipedia sur le symbole prédit.

### **Guide d'Utilisation**

#### **Étape 1 : Dessiner et Enregistrer un Symbole**

1. Lancez le script `Drawer.py` :
   ```bash
   python Drawer.py
   ```
2. Utilisez l'interface graphique pour dessiner un symbole. Sauvegardez-le en entrant un nom de fichier.

---

#### **Étape 2 : Entraînement du Modèle MLP**

1. Lancez le script `mlp.py` pour entraîner le modèle de reconnaissance de symboles :
   ```bash
   python mlp.py
   ```
2. Le modèle entraîné sera sauvegardé sous le nom `mlp_symbol_recognition.pkl`.

---

#### **Étape 3 : Prédiction et Recherche Wikipedia**

1. Lancez le script `wiki_search.py` :
   ```bash
   python wiki_search.py
   ```
2. Dessinez un symbole et cliquez sur **Prédire** pour :
   - Identifier le symbole.
   - Rechercher des informations correspondantes sur Wikipedia.
   - Afficher un résumé synthétique et des graphiques associés.

---

#### **Étape 4 : Visualisation des Liens et Références**

1. Utilisez les scripts `graphe_lien.py` et `graphe_ref.py` pour générer des graphiques des liens externes et des références respectivement.
   - Pour les liens externes :
     ```bash
     python graphe_lien.py
     ```
   - Pour les références externes :
     ```bash
     python graphe_ref.py
     ```

---

### **Organisation des Fichiers**

- **Scripts principaux** :
  - `Drawer.py`, `mlp.py`, `wiki_search.py`
  - `graphe_lien.py`, `graphe_ref.py`
- **Données générées** :
  - Modèle sauvegardé : `mlp_symbol_recognition.pkl`
  - Fichiers texte des symboles : `.txt`
  - Graphiques des liens et références : `.png`

---

### **Fonctionnalités Clés**

1. Dessin de symboles via une interface graphique interactive.
2. Reconnaissance de symboles avec un modèle MLP.
3. Recherche et résumé de pages Wikipedia basés sur les symboles reconnus.
4. Visualisation des liens externes et des références sous forme de graphiques.

---

### **Installation des Dépendances**

1. Installez les bibliothèques requises :

   ```bash
   pip install -r requirements.txt
   ```

2. Téléchargez les ressources linguistiques :

   ```bash
   python -m nltk.downloader punkt
   ```

---
