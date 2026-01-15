import streamlit as st
import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
    host="localhost",
    user="python_user", 
    password="",          
    database="Extraction",
    port=3306
    )

conn = get_connection()

patients = pd.read_sql("SELECT patient_id, CONCAT(first_name, ' ', last_name) as name FROM patients", conn)

st.title("Inserer les données du patients ")
prenom = st.text_input("Nom du patient (ex: David)")
nom = st.text_input("Nom du patient (ex: Williams)")
annee = st.text_input("Année de naissance (ex: 1955-06-04)")
pid = st.text_input("ID du patient (ex: P001)")

if st.button("Valider"):
    st.session_state['patient_filters'] = {
        "prenom": prenom,
        "nom": nom,
        "date_naissance": annee,
        "pid": pid
    }
    st.session_state['patient_found'] = False   # on reset pour éviter l’affichage auto

# ============= Recherche du patient =============
if 'patient_filters' in st.session_state and not st.session_state.get('patient_found', False):

    f = st.session_state['patient_filters']

    query = f"""
        SELECT patient_id, first_name, last_name, date_of_birth
        FROM patients
        WHERE (
            first_name = '{f['prenom']}'
            AND last_name = '{f['nom']}'
            AND date_of_birth = '{f['date_naissance']}'
        )
        OR patient_id = '{f['pid']}'
    """

    patient = pd.read_sql(query, conn)

    if patient.empty:
        st.warning("Aucun patient trouvé.")
        st.session_state['patient_found'] = False
    else:
        st.session_state['patient_found'] = True
        st.session_state['patient_id'] = patient.iloc[0]['patient_id']
        st.success(f"Patient trouvé : {patient.iloc[0]['first_name']} {patient.iloc[0]['last_name']}")
        st.info("Sélectionner un profil à afficher dans le menu ci-dessous.")

# ============= Choix du profil =============
if st.session_state.get('patient_found', False):

    profil_choice = st.selectbox(
        "Quel profil voulez-vous afficher ?",
        ["", "Profil Social", "Profil Médical", "Profil Financier"]
    )

    commande = st.text_input("Ou tapez une commande (ex: 'je veux le profil financier')")
    profil_cmd = None

    if st.button("Interpréter la commande"):
        cmd = commande.lower()

        if "financ" in cmd:
            profil_cmd = "Profil Financier"
        elif "médic" in cmd or "medical" in cmd:
            profil_cmd = "Profil Médical"
        elif "social" in cmd:
            profil_cmd = "Profil Social"
        else:
            st.warning("Commande non reconnue. Essayez 'social', 'médical' ou 'financier'.")    


    # ============= Affichage du profil =============
    profil_to_show = profil_cmd if profil_cmd else profil_choice

    if profil_to_show and profil_to_show != "":
        pid_val = st.session_state['patient_id']

        if profil_to_show == "Profil Social":
            data = pd.read_sql(f"SELECT * FROM profil_social WHERE patient_id = '{pid_val}'", conn)
            st.subheader("Profil Social")
            st.dataframe(data)

        elif profil_to_show == "Profil Médical":
            data = pd.read_sql(f"SELECT * FROM profil_medical WHERE patient_id = '{pid_val}'", conn)
            st.subheader("Profil Médical")
            st.dataframe(data)

        elif profil_to_show == "Profil Financier":
            data = pd.read_sql(f"SELECT * FROM profil_financier WHERE patient_id = '{pid_val}'", conn)
            st.subheader("Profil Financier")
            st.dataframe(data)