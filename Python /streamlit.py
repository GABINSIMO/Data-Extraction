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
    query = f"""
        SELECT patient_id, first_name, last_name, date_of_birth
        FROM patients
        WHERE (last_name = '{nom}' 
        AND first_name = '{prenom}' 
        AND date_of_birth = '{annee}'
        ) OR patient_id = '{pid}'
    """
    patient = pd.read_sql(query, conn)

    if patient.empty:
        st.warning("Aucun patient trouvé.")
    else:
        patient_id = patient.iloc[0]['patient_id']
        st.success(f"Patient trouvé : {patient.iloc[0]['first_name']} {patient.iloc[0]['last_name']} ({patient_id})")

        # PROFIL SOCIAL
        social = pd.read_sql(f"SELECT * FROM profil_social WHERE patient_id = '{patient_id}'", conn)
        st.subheader("Profil Social")
        st.dataframe(social)

        # PROFIL MÉDICAL
        medical = pd.read_sql(f"SELECT * FROM profil_medical WHERE patient_id = '{patient_id}'", conn)
        st.subheader("Profil Médical")
        st.dataframe(medical)

        # PROFIL FINANCIER
        financial = pd.read_sql(f"SELECT * FROM profil_financier WHERE patient_id = '{patient_id}'", conn)
        st.subheader("Profil Financier")
        st.dataframe(financial)