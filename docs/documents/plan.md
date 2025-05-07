# Plan de Développement : Protocole Graphique Hexagonal

## Objectif Général

Concevoir et implémenter un protocole de communication graphique original et robuste, basé sur une matrice de cellules hexagonales. Le système devra permettre d'encoder un message texte en une image graphique et, idéalement, de pouvoir la décoder en tenant compte des altérations courantes (rotation, mise à l'échelle, bruit, erreurs).

## Phase 1: Conception et Spécification Détaillée du Protocole

L'objectif de cette phase est de définir précisément toutes les règles et composants du protocole graphique hexagonal.

### 1.1. Structure de la Matrice
  - **Forme Générale :** Probablement carrée ou rectangulaire globalement, mais pavée d'hexagones.
  - **Cellules Hexagonales :**
    - **Unité d'information :** 2 bits par hexagone.
    - **Set de Couleurs (Valeurs RVB idéales) :**
        1.  Noir (N) : `(0, 0, 0)`
        2.  Rouge (R) : `(255, 0, 0)`
        3.  Bleu (L) : `(0, 0, 255)` (L pour bLeu)
        4.  Blanc (B) : `(255, 255, 255)`
    - **Mapping Bits-Couleurs :**
        - `00` -> Noir
        - `01` -> Rouge
        - `10` -> Bleu
        - `11` -> Blanc
    - **Logique du Mapping :** Utilisation des extrêmes achromatiques (Noir pour `00`, Blanc pour `11`) pour un contraste maximal et une progression logique, avec les couleurs chromatiques primaires (Rouge, Bleu) pour les valeurs intermédiaires.
  - **Tailles de Matrice :** Définir plusieurs tailles fixes (versions du protocole) pour accommoder différentes longueurs de message. Chaque version aura un nombre spécifique d'hexagones.

### 1.2. Repères d'Alignement et d'Orientation (Finder Patterns)
  - **Rôle :** Permettre la détection de la matrice, la correction de la rotation, de la perspective et de la mise à l'échelle.
  - **Nombre :** Trois repères principaux.
  - **Position :** Placés aux coins logiques de la zone de données (ex: Haut-Gauche, Haut-Droit, Bas-Gauche).
  - **Conception Détaillée :**
    - Chaque repère est une structure de 7 hexagones (un hexagone central entouré d'un anneau de 6 hexagones).
    - **Repère 1 (Origine - ex: Haut-Gauche) :** Hexagone central Blanc, anneau de 6 hexagones Rouges.
    - **Repère 2 (Axe X - ex: Haut-Droit) :** Hexagone central Blanc, anneau de 6 hexagones Rouges.
    - **Repère 3 (Axe Y - ex: Bas-Gauche) :** Hexagone central Blanc, anneau de 6 hexagones Bleus.
    - Cette configuration (2x Blanc/Rouge, 1x Blanc/Bleu) assure l'unicité et permet de lever l'ambiguïté sur l'orientation.

### 1.3. Motifs de Synchronisation (Timing Patterns)
  - **Rôle :** Aider à localiser précisément les centres des hexagones de données après la transformation géométrique globale et compenser les distorsions locales.
  - **Couleurs Utilisées :** Alternance Noir et Blanc (pour un contraste maximal).
  - **Emplacement :**
    - Une ligne d'hexagones alternés Noir/Blanc s'étendant entre le Repère 1 (Origine) et le Repère 2 (Axe X).
    - Une ligne d'hexagones alternés Noir/Blanc s'étendant entre le Repère 1 (Origine) et le Repère 3 (Axe Y).
    - Ces lignes sont adjacentes à la zone de données principale.

### 1.4. Patchs de Calibration des Couleurs
  - **Rôle :** Fournir des références de couleurs exactes au décodeur.
  - **Nombre et Composition :** Quatre hexagones simples (même taille que les cellules de données), chacun avec une des couleurs du protocole : Noir, Rouge, Bleu, Blanc.
  - **Emplacement :** Un groupe de 4 hexagones adjacents (ex: en ligne ou en L), placé dans une position fixe et connue, par exemple à proximité immédiate du Repère 1 (Origine), en dehors de la zone de données et des motifs de synchronisation.
  - **Ordre :** L'ordre des couleurs dans ce groupe de patchs est fixe (ex: Noir - Rouge - Bleu - Blanc).

### 1.5. Métadonnées
  - **Types d'Information :**
    - Version du protocole / Taille de la matrice.
    - Longueur du message encodé.
    - Type et niveau de Code Correcteur d'Erreurs (ECC) utilisé.
    - (Implicit) La présence et la définition des patchs de calibration sont inhérentes à la version du protocole.
    - (Optionnel) Indicateurs pour des fonctionnalités avancées (ex: compression de données, type de contenu).
  - **Localisation :** Une ou plusieurs zones dédiées dans la matrice, protégées par leur propre ECC simple si nécessaire. Leur position doit être fixe ou facilement déductible à partir des repères.

### 1.6. Données du Message
  - **Encodage :** Conversion du texte en binaire, puis groupement des bits par paires (`00`, `01`, `10`, `11`) pour l'assignation des couleurs Noir, Rouge, Bleu, Blanc respectivement.
  - **Placement :** Remplissage des hexagones de données avec les couleurs correspondantes, selon un chemin de lecture défini.

### 1.7. Correction d'Erreurs (ECC)
  - **Stratégie :** Utilisation d'un code correcteur d'erreurs robuste.
  - **Choix Pressenti :** Reed-Solomon.
  - **Niveaux de Correction :** Définir différents niveaux de redondance, stockés dans les métadonnées.
  - **Entrelacement (Interleaving) :** Les symboles de données (représentant les couleurs/groupes de bits) et les symboles d'ECC seront entrelacés.

### 1.8. Chemin de Lecture/Écriture des Données
  - Définir un parcours standardisé pour lire/écrire les symboles de couleur dans les hexagones.

### 1.9. Capacité de Données
  - Calculer la capacité théorique (en bits) pour chaque taille de matrice et niveau d'ECC, en tenant compte du nombre de bits par cellule couleur.

## Phase 2: Spécification des Algorithmes d'Encodage et de Décodage

### 2.1. Algorithme d'Encodage (Texte -> Image Graphique)
  1. Prise en entrée du message texte.
  2. (Optionnel) Compression du message.
  3. Conversion du texte en flux binaire.
  4. Sélection de la taille de matrice appropriée et du niveau d'ECC.
  5. Groupement des bits du message en symboles (ex: 2 bits par symbole).
  6. Calcul et ajout des symboles d'ECC (sur les symboles de données).
  7. Encodage des métadonnées.
  8. Entrelacement des symboles de données et des symboles d'ECC.
  9. Construction de la matrice :
    - Placement des Repères d'Alignement (selon 1.2).
    - Placement des Motifs de Synchronisation (selon 1.3).
    - Placement des Patchs de Calibration des Couleurs (selon 1.4).
    - Placement des Métadonnées (selon 1.5).
    - Assignation des couleurs aux hexagones de données basé sur les symboles entrelacés (selon 1.6), selon le chemin de lecture (1.8).
  10. Génération de l'image graphique finale.

### 2.2. Algorithme de Décodage (Image Graphique -> Texte)
  1. Prise en entrée de l'image.
  2. Prétraitement de l'image (lissage, etc., mais pas nécessairement binarisation si travail en couleur).
  3. Détection des Repères d'Alignement.
  4. Calcul de la Transformation Géométrique.
  5. Identification et Lecture des Patchs de Calibration des Couleurs :
    - Établir les références de couleurs réelles pour le set utilisé.
  6. Identification et Lecture des Motifs de Synchronisation.
  7. Lecture des Métadonnées (en utilisant les couleurs calibrées).
  8. Lecture des Hexagones de Données :
    - Pour chaque hexagone, déterminer sa couleur dominante.
    - Classifier la couleur lue en utilisant les références calibrées pour la faire correspondre à l'une des couleurs du protocole.
    - Convertir la couleur classifiée en symbole de bits (ex: 2 bits).
  9. Désentrelacement des symboles lus.
  10. Application du Code Correcteur d'Erreurs sur les symboles.
  11. Reconstruction du flux binaire du message à partir des symboles corrigés.
  12. (Optionnel) Décompression du message.
  13. Conversion du binaire en texte.
  14. Sortie du message texte décodé.

## Phase 3: Choix Technologiques et Environnement de Développement
 (Peu de changements ici, mais la bibliothèque ECC devra gérer des symboles non binaires si Reed-Solomon est appliqué sur des symboles de q-bits)

### 3.1. Langage de Programmation
  - **Principalement envisagé :** Python.
  - Justification : Prototypage rapide, écosystème scientifique mature.

### 3.2. Bibliothèques Clés
  - **Génération d'Image (Encodeur) :** Pillow.
  - **Traitement d'Image (Décodeur) :** OpenCV (pour détection de formes, transformations, lecture de couleurs, classification de couleurs).
  - **ECC :** Recherche d'une bibliothèque Python pour Reed-Solomon capable de travailler sur des symboles de Galois Field GF(2^m) où m est le nombre de bits par symbole couleur.

### 3.3. Outils de Développement
  - **Gestion de Version :** Git.
  - **IDE :** VS Code, PyCharm, etc.
  - **Tests :** PyTest ou `unittest`.

## Phase 4: Développement du Programme d'Encodage
 (Les modules devront gérer l'assignation des couleurs)

### 4.1. Module de Gestion de la Grille Hexagonale
  - Fonctions pour calculer les positions des centres des hexagones.
  - Gestion des coordonnées hexagonales.

### 4.2. Module de Génération des Éléments de Structure
  - Dessin des repères d'alignement (en couleur).
  - Dessin des motifs de synchronisation (en couleur).
  - Dessin des patchs de calibration.

### 4.3. Module d'Encodage des Données et Métadonnées
  - Conversion texte vers binaire, puis vers symboles de couleur.
  - Formatage des métadonnées.

### 4.4. Module ECC
  - Intégration d'une fonction pour calculer les symboles de Reed-Solomon sur GF(2^m).

### 4.5. Module d'Entrelacement
  - Implémentation du schéma d'entrelacement sur les symboles de couleur.

### 4.6. Module Principal de l'Encodeur et Génération d'Image
  - Orchestration et création de l'image finale en couleur.

## Phase 5: Développement du Programme de Décodage
 (Les modules devront gérer la lecture et classification des couleurs)

### 5.1. Module de Chargement et Prétraitement d'Image
  - Lecture de l'image en couleur.
  - Potentiellement des étapes de normalisation des couleurs, lissage.

### 5.2. Module de Détection des Repères
  - Algorithmes de détection de formes/couleurs.

### 5.3. Module de Transformation Géométrique
  - Idem.

### 5.4. Module de Lecture des Cellules et Calibration
  - Lecture des patchs de calibration.
  - Localisation des centres des hexagones.
  - Échantillonnage des couleurs et classification par rapport aux références calibrées.
  - Conversion en symboles de bits.

### 5.5. Module de Désentrelacement et Correction ECC
  - Application inverse de l'entrelacement sur les symboles.
  - Utilisation du décodeur Reed-Solomon sur GF(2^m).

### 5.6. Module Principal du Décodeur
  - Orchestration et extraction du message.

## Phase 6: Tests, Itérations et Améliorations

### 6.1. Tests Unitaires et d'Intégration
  - Idem.

### 6.2. Tests de Robustesse
  - Inclure des tests spécifiques à la dégradation des couleurs (variations d'éclairage lors du scan/photo, impression sur différents papiers/imprimantes).

### 6.3. Itérations et Optimisations
  - Affiner les algorithmes de classification des couleurs.
  - Optimiser les seuils de décision pour les couleurs.

### 6.4. Exploration de la Densité/Robustesse des Couleurs
  - Tester différents sets de couleurs (plus ou moins de couleurs, différentes teintes).
  - Évaluer l'impact sur la robustesse vs densité.
  - Affiner les algorithmes de calibration et de classification des couleurs.

### 6.5. (Optionnel - Sujet TP) Intégration de Logo
  - Idem.

## Phase 7: Rédaction du Rapport Détaillé
 (La justification des choix de couleurs, de leur mapping et de leur gestion sera importante)

### 7.1. Présentation du Protocole
  - Inclure la spécification du set de couleurs (avec valeurs RVB idéales), le mapping bits-couleurs et sa justification, la description détaillée des Repères d'Alignement, des Motifs de Synchronisation, et des Patchs de Calibration (composition, emplacement, rôle).

### 7.2. Spécification des Algorithmes
  - Détailler les étapes de calibration et de classification des couleurs.

### 7.3. Capacités et Limitations
  - Discuter de la sensibilité aux altérations de couleurs.

### 7.4. Guide d'Utilisation du Programme
  - Idem.

### 7.5. Choix Technologiques
  - Justifier le choix des bibliothèques pour la gestion des couleurs et l'ECC sur symboles.

## Annexes (Optionnel)
  - Exemples d'images générées (en couleur).
  - Résultats des tests de robustesse des couleurs.
