# Extraction d'informations et Analyse de Compétences depuis un CV PDF
Dans ce projet, j'ai utilisé Streamlit, spaCy, et pdfplumber pour extraire des informations pertinentes depuis des fichiers PDF de CV. L'objectif est de fournir une application simple et interactive qui permet de traiter plusieurs CVs à la fois et d'en extraire automatiquement des informations telles que le nom, l'email, le téléphone, les compétences, les langues et les diplômes. En plus de l'extraction des informations de base, l'application analyse également le texte pour détecter des compétences spécifiques basées sur une liste prédéfinie (comme Python, Excel, Machine Learning, etc.). Si une compétence est trouvée, elle est marquée avec un symbole validé, et si la compétence n'est pas présente dans la liste, l'utilisateur peut l'ajouter à la liste des compétences pour une détection future.
## Objectifs du Projet
- Extraction de texte depuis un PDF : J'ai développé une fonctionnalité permettant de télécharger un ou plusieurs fichiers PDF de CV. L'application extrait ensuite le texte brut des fichiers PDF grâce à la bibliothèque pdfplumber.
- Traitement du langage naturel : J'ai utilisé le modèle de traitement du langage naturel spaCy pour analyser le texte et en extraire les entités pertinentes comme le nom, l'email et les compétences. Le modèle est spécialement configuré pour traiter la langue française.
- Détection des compétences : L'application analyse le texte pour détecter des compétences spécifiques basées sur une liste prédéfinie (comme Python, Excel, Machine Learning, etc.). Si une compétence est trouvée, elle est marquée avec un symbole validé. Si la compétence n'est pas présente dans la liste, l'utilisateur peut l'ajouter à la liste des compétences pour une détection future. 
- Extraction d'autres informations : En plus des compétences, l'application extrait également des informations comme les langues parlées, les diplômes et le numéro de téléphone (si présents dans le CV).
- Interface Streamlit : L'application offre une interface graphique simple où l'utilisateur peut télécharger des fichiers PDF, entrer des compétences personnalisées, et visualiser les résultats d'extraction sous forme de tableau. Il est également possible de télécharger les résultats sous forme de fichier CSV.
- Sauvegarde des données : Après l'extraction des informations, l'utilisateur peut choisir de sauvegarder les résultats dans un fichier CSV ou JSON pour une utilisation ultérieure.
## Technologies utilisées
- Streamlit : Pour la création de l'interface web interactive.
- pdfplumber : Pour l'extraction du texte des fichiers PDF.
- spaCy : Pour l'extraction des entités (nom, email, etc.) et le traitement du langage naturel.
- JSON / CSV : Pour la gestion des compétences et la sauvegarde des données extraites.

<p align="center">
  <a href="https://www.linkedin.com/in/ikram-nefzi-7019741b1/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>
