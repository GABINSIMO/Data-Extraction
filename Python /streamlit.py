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

st.title("Selectionner le profil")

selected_patient = st.selectbox("Choisir un patient", patients['patient_id'], format_func=lambda x: patients.set_index('patient_id').loc[x, 'name'])

if st.button("Afficher les profils"):
    # Profil social
    social = pd.read_sql(f"SELECT * FROM profil_social WHERE patient_id = '{selected_patient}'", conn)
    st.subheader("Profil Social")
    st.dataframe(social)

    # Profil médical
    medical = pd.read_sql(f"SELECT * FROM profil_medical WHERE patient_id = '{selected_patient}'", conn)
    st.subheader("Profil Médical")
    st.dataframe(medical)

    # Profil financier
    financial = pd.read_sql(f"SELECT * FROM profil_financier WHERE patient_id = '{selected_patient}'", conn)
    st.subheader("Profil Financier")
    st.dataframe(financial)