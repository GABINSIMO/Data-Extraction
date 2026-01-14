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

if st.button("Rechercher"):
    st.session_state['patient_query'] = f"""
        SELECT patient_id, first_name, last_name, date_of_birth
        FROM patients
        WHERE (
            first_name = '{prenom}'
            AND last_name = '{nom}'
            AND date_of_birth = '{annee}'
        )
        OR patient_id = '{pid}'
    """

# Si une recherche a été stockée
if 'patient_query' in st.session_state:
    patient = pd.read_sql(st.session_state['patient_query'], conn)

    if patient.empty:
        st.warning("Aucun patient trouvé.")
    else:
        patient_id = patient.iloc[0]['patient_id']
        st.success(f"Patient : {patient.iloc[0]['first_name']} {patient.iloc[0]['last_name']} ({patient_id})")

        profil_choice = st.selectbox(
            "Quel profil afficher ?",
            ["Profil Social", "Profil Médical", "Profil Financier"]
        )

        if profil_choice == "Profil Social":
            data = pd.read_sql(f"SELECT * FROM profil_social WHERE patient_id = '{patient_id}'", conn)
            st.dataframe(data)

        if profil_choice == "Profil Médical":
            data = pd.read_sql(f"SELECT * FROM profil_medical WHERE patient_id = '{patient_id}'", conn)
            st.dataframe(data)

        if profil_choice == "Profil Financier":
            data = pd.read_sql(f"SELECT * FROM profil_financier WHERE patient_id = '{patient_id}'", conn)
            st.dataframe(data)