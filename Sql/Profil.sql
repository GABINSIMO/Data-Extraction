/*
------------------------------------------------------------------
                       Profil Social 
------------------------------------------------------------------
*/


CREATE VIEW profil_social AS
SELECT 
	patient_id,
	CONCAT(first_name, ' ',last_name) AS nom_patient,
    gender AS genre,
    date_of_birth AS Date_naissance,
    contact_number AS Telephone,
    address AS Adresse,
    registration_date AS Enregistrement, 
    insurance_provider AS Assurance,
    insurance_number AS Numero_assurance,
    email
FROM patients;


/*
------------------------------------------------------------------
                       Profil Financier 
------------------------------------------------------------------
*/


CREATE OR REPLACE VIEW Profil_financier AS
SELECT 
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS nom_patient,
    
    COUNT(DISTINCT t.treatment_id) AS Nb_traitement,

    SUM(f.amount) AS Total_facture,
    SUM(CASE WHEN f.payment_status = 'Paid' THEN f.amount ELSE 0 END) AS Total_Paiement,
    SUM(CASE WHEN f.payment_status <> 'Paid' THEN f.amount ELSE 0 END) AS Total_non_payé,

    SUM(CASE WHEN f.payment_method = 'Insurance' THEN f.amount ELSE 0 END) AS Couverture_Assurance,
    SUM(CASE WHEN f.payment_method <> 'Insurance' THEN f.amount ELSE 0 END) AS Total_a_depenser,

    ROUND(
        SUM(CASE WHEN f.payment_method = 'Insurance' THEN f.amount ELSE 0 END) / NULLIF(SUM(f.amount),0) * 100,
        2
    ) AS Pourcentage_assurance,

    MIN(f.bill_date) AS date_paiement_1,
    MAX(f.bill_date) AS date_paiement_derneir

FROM patients p
LEFT JOIN rdv r 
	ON p.patient_id = r.patient_id
LEFT JOIN traitements t 
	ON r.appointment_id = t.appointment_id
LEFT JOIN factures f 
	ON t.treatment_id = f.treatment_id

GROUP BY p.patient_id, nom_patient;


/*
------------------------------------------------------------------
                       Profil medical 
------------------------------------------------------------------
*/

CREATE OR REPLACE VIEW profil_medical AS
SELECT 
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS nom_patient,

    COUNT(DISTINCT r.appointment_id) AS Rdv_Total,
    COUNT(DISTINCT t.treatment_id) AS Nb_traitements,

    GROUP_CONCAT(DISTINCT d.specialization ORDER BY d.specialization SEPARATOR ', ') AS Specialisation,
    GROUP_CONCAT(DISTINCT t.treatment_type ORDER BY t.treatment_type SEPARATOR ', ') AS Traitement,
    GROUP_CONCAT(DISTINCT r.reason_for_visit ORDER BY r.reason_for_visit SEPARATOR ', ') AS Raison,

    MIN(t.treatment_date) AS date_paiement_1,
    MAX(t.treatment_date) AS date_paiement_derneir,

    DATEDIFF(MAX(t.treatment_date), MIN(t.treatment_date)) AS Durée_medicale,

    ROUND(COUNT(t.treatment_id) / NULLIF(DATEDIFF(MAX(t.treatment_date), MIN(t.treatment_date)),0), 2) AS Traitement_Jour

FROM patients p
LEFT JOIN rdv r 
	ON p.patient_id = r.patient_id
LEFT JOIN traitements t 
	ON r.appointment_id = t.appointment_id
LEFT JOIN docteurs d 
	ON r.doctor_id = d.doctor_id

GROUP BY p.patient_id, nom_patient;



