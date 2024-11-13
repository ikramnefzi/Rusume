import streamlit as st
import pdfplumber
import spacy
import json
import re
import pandas as pd
import os
from streamlit_tags import st_tags

# Charger le modèle NLP de spaCy pour le français
nlp = spacy.load("fr_core_news_sm")

# Charger les compétences depuis un fichier JSON
skills_file = "skills.json"

# Charger les compétences depuis un fichier JSON
def load_skills():
    if os.path.exists(skills_file):
        with open(skills_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return ["Python", "Excel", "Machine Learning", "Data Analysis", "Java", "Tableau",
            "Power BI", "Microsoft Excel", "HTML", "CSS", "R"]

# Sauvegarder les compétences dans un fichier JSON
def save_skills(skills):
    with open(skills_file, "w", encoding="utf-8") as file:
        json.dump(skills, file, ensure_ascii=False, indent=4)

# Fonction pour ajouter une compétence automatiquement si elle n'existe pas
def add_skill_if_not_exists(skill):
    """Ajoute la compétence au fichier JSON si elle n'existe pas déjà."""
    skills_keywords = load_skills()  # Charger les compétences existantes du fichier
    if skill.lower() not in [s.lower() for s in skills_keywords]:
        skills_keywords.append(skill)  # Ajouter la compétence à la liste
        save_skills(skills_keywords)  # Sauvegarder la liste mise à jour dans le fichier JSON
        return f"Compétence '{skill}' ajoutée au fichier JSON."
    else:
        return f"Compétence '{skill}' déjà présente dans le fichier JSON."

# Extraction de compétences
def extract_skills(text, skills_keywords=None):
    """Détecte certaines compétences techniques basées sur des mots-clés, avec ajout automatique si nécessaire."""
    if skills_keywords is None:
        skills_keywords = load_skills()  # Charger les compétences depuis le fichier
    skills_with_validation = []
    for skill in skills_keywords:
        if skill.lower() in text.lower():
            skills_with_validation.append(f"{skill} ✅")  # Symbole validé
        else:
            skills_with_validation.append(f"{skill} ❌")  # Symbole non validé

        # Ajouter la compétence au fichier JSON si elle n'est pas trouvée
        if skill.lower() not in text.lower():
            add_skill_if_not_exists(skill)  # Ajouter automatiquement si non trouvée

    return skills_with_validation if skills_with_validation else ["Compétences non trouvées"]

# Ajouter une compétence à la liste
#def add_skill():
    # Load the skills_keywords when the function is called
    #skills_keywords = load_skills()
    #new_skill = input("Entrez une compétence à ajouter (ou tapez 'fin' pour terminer) : ")
    #if new_skill.lower() != 'fin' and new_skill not in skills_keywords:
        # Update skills_keywords, as it is now local to this function.
        #skills_keywords.append(new_skill)
        #save_skills(skills_keywords)  # Sauvegarder les compétences mises à jour
       # print(f"La compétence '{new_skill}' a été ajoutée.")
    #else:
        #print("Aucune compétence ajoutée.")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_name(text):
    doc = nlp(text)
    candidat_nom = None
    for ent in doc.ents:
        if ent.label_ == "PER" and ent.start_char < 200:
            candidat_nom = ent.text
            break
    if not candidat_nom:
        words = text.split()
        candidat_nom = " ".join(words[:2]) if len(words) >= 2 else "Nom non trouvé"
    return candidat_nom

def extract_email(text):
    doc = nlp(text)
    for token in doc:
        if token.like_email:
            return token.text
    return "Email non trouvé"

def extract_phone(text):
    phone_pattern = r"\+?\d[\d -]{8,12}\d"
    phone_match = re.search(phone_pattern, text)
    return phone_match.group(0) if phone_match else "Téléphone non trouvé"

def extract_languages(text):
    known_languages = ["français", "anglais", "espagnol", "allemand", "italien", "arabe", "chinois"]
    found_languages = [lang.capitalize() for lang in known_languages if lang in text.lower()]
    return found_languages if found_languages else ["Langues non trouvées"]

def extract_diploma(text):
    doc = nlp(text)
    diplomas = []
    diploma_keywords = ["bac", "master", "licence", "doctorat", "mastère"]
    for sent in doc.sents:
        for keyword in diploma_keywords:
            if keyword.lower() in sent.text.lower():
                diplomas.append(sent.text.strip())
                break
    return diplomas if diplomas else ["Diplôme non trouvé"]

# Fonction pour vérifier si une compétence est présente et retourner un symbole
def get_validation_symbol(skill, text):
    """Retourne un symbole de validation pour une compétence trouvée dans le texte."""
    if skill.lower() in text.lower():
        return f"{skill} ✅"  # Symbole validé
    else:
        return f"{skill} ❌"  # Symbole non validé

# Interface Streamlit
st.title("Extraction d'informations depuis un CV PDF")

# Ajout des liens LinkedIn et GitHub
st.markdown(
    """
    <style>
    .container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .button {
        display: inline-flex;
        align-items: center;
        padding: 10px 20px;
        font-size: 16px;
        color: black;
        background-color: #f0f0f0; /* Couleur de fond grise */
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
        margin-right: 10px;
        border: 2px solid;
    }
    .button.linkedin {
        border-color: #0072b1; /* Bordure bleue pour LinkedIn */
    }
    .button.github {
        border-color: #333; /* Bordure noire pour GitHub */
    }
    .button img {
        width: 20px;
        height: 20px;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="container">
        <a href="https://www.linkedin.com/in/ikram-nefzi-7019741b1/" class="button linkedin" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn Logo"> LinkedIn
        </a>
        <a href="https://github.com/ikramnefzi/Rusume" class="button github" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub Logo"> GitHub
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Charger les compétences depuis le fichier JSON
skills_keywords = ["Python", "Excel", "Machine Learning"] #load_skills()

# Afficher les compétences sous forme de tags
selected_skills = st_tags(
    label='Entrez les compétences :',
    text='Appuyez sur entrée pour ajouter plus',
    value=skills_keywords,
    suggestions=["Python", "Excel", "Machine Learning", "Data Analysis"],
    key='1'
)

if selected_skills:
    save_skills(selected_skills)

# Charger plusieurs fichiers PDF pour extraction
uploaded_files = st.file_uploader("Choisissez plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    cv_data_list = []  # Liste pour stocker les données de tous les CVs extraits
    for uploaded_file in uploaded_files:
        text = extract_text_from_pdf(uploaded_file)

        # Extraction des informations du CV
        cv_data = {
            'Nom': extract_name(text),
            'Email': extract_email(text),
            'Téléphone': extract_phone(text),
            'Compétences': extract_skills(text, selected_skills),
            'Langues': extract_languages(text),
            'Diplôme': extract_diploma(text),
        }

        cv_data_list.append(cv_data)  # Ajouter les données du CV à la liste

    # Afficher les données de tous les CVs
    st.subheader("Informations extraites de tous les CVs")

    # Convertir en DataFrame pour affichage
    df_cv_data = pd.DataFrame(cv_data_list)
    st.write("Données sous forme de tableau :")
    st.dataframe(df_cv_data)

    # Option de sauvegarder en JSON
    #if st.button("Sauvegarder en JSON"):
        #with open("informations_CV.json", "w", encoding="utf-8") as file:
            #json.dump(cv_data_list, file, ensure_ascii=False, indent=4)
        #st.success("Les informations ont été sauvegardées dans le fichier JSON.")

    # Option de sauvegarder en CSV et télécharger
    st.markdown("---")  # Séparateur visuel

    # Convertir le DataFrame en CSV
    csv = df_cv_data.to_csv(index=False).encode('utf-8')

    # CSS pour personnaliser et centrer le bouton de téléchargement
    st.markdown(
        """
        <style>
        .centered-button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .stDownloadButton > button {
            background-color: #f0f0f0;  /* gris clair */
            color: #333;                /* noir */
            font-weight: bold;          /* texte en gras */
            border: 2px solid #000;     /* bordure noire */
            padding: 8px 16px;
            border-radius: 5px;
        }
        .stDownloadButton > button:hover {
            background-color: #e0e0e0;  /* gris plus foncé au survol */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Ajouter le bouton de téléchargement au centre de la page
    st.markdown('<div class="centered-button-container">', unsafe_allow_html=True)
    st.download_button(
        label="Télécharger les données en CSV",
        data=csv,
        file_name='informations_CV.csv',
        mime='text/csv',
    )
    st.markdown('</div>', unsafe_allow_html=True)

    #Afficher JSON
    for i, cv_data in enumerate(cv_data_list):
        st.write(f"**CV {i + 1}:**")
        st.write(cv_data)


