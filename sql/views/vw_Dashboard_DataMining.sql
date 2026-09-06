USE [DW_TFG];
GO

CREATE OR ALTER VIEW vw_Dashboard_DataMining AS
SELECT 
    -- 1. Dimensión Paciente / Demografía
    p.Gender,
    p.Ethnicity,
    a.Age,
    a.AdmissionHeight,
    a.AdmissionWeight,
    a.DischargeWeight,

    -- 2. Dimensión Hospitalaria (Reducida)
    u.Type AS UnitType,
    u.StayType AS UnitStayType,
    
    -- 3. Dimensión Diagnóstico de Admisión
    ad.ApacheAdmissionDx AS DiagnosisAdmission,
    s.Service AS Service,
    
    -- 4. Variables Fisiológicas al Ingreso y Scores Clínicos
    a.APS,
    a.ApacheScore,
    a.HeartRate AS HeartRate_Admission,
    a.MeanBP AS MeanBP_Admission,
    a.Temperature,
    a.RespiratoryRate AS RespiratoryRate_Admission,
    
    -- 5. Indicadores Clínicos / Flags (0 o 1)
    a.DiedInHospital, -- Target Modelo 1
    a.Intubated,
    a.Vent,
    a.Dialysis,
    a.ActiveTreatment,
    a.ElectiveSurgery,
    
    -- 6. Comorbilidades
    a.Diabetes,
    a.Cirrhosis,
    a.HepaticFailure,
    a.MetastaticCancer,
    a.Leukemia,
    a.Lymphoma,
    a.Immunosuppression,
    a.MI,

    -- 7. Escala de Glasgow, Soporte e Historial (0% - 4% Nulos)
    a.Eyes,
    a.Motor,
    a.Verbal,
    a.VentApacheDay,
    a.IntubApacheDay,
    a.Thrombolytics,
    a.IMA,
    a.HasPhysicalExam,
    a.PastHistory,
    a.Meds,

    -- 8. Analíticas de Laboratorio Básicas (12% - 25% Nulos)
    a.Glucose,
    a.Sodium,
    a.Creatinine,
    a.BUN,
    a.Hematocrit,
    a.WBC,

    -- =======================================================
    -- 9. VARIABLES DE TIEMPO (Necesarias para Regresión LoS)
    -- =======================================================
    
    -- Dimensión Tiempo (Ingreso)
    t_admit.Year AS AdmitYear,
    t_admit.DayNumber AS AdmitDayNumber,
    t_admit.Hour AS AdmitHour,

    -- Dimensión Tiempo (Alta)
    t_discharge.Year AS DischargeYear,
    t_discharge.DayNumber AS DischargeDayNumber,
    t_discharge.Hour AS DischargeHour

FROM AdmittedToICU a
LEFT JOIN PatientUnitStay pus ON a.PatientUnitStayFK = pus.PatientUnitStayID
LEFT JOIN PatientHealthSystem phs ON pus.PatientHealthSystemFK = phs.PatientHealthSystemID
LEFT JOIN Patient p ON phs.PatientFK = p.PatientID
LEFT JOIN Unit u ON a.UnitFK = u.UnitID
LEFT JOIN AdmissionDiagnosis ad ON a.AdmDiagFK = ad.AdmDiagID
LEFT JOIN Service s ON ad.ServiceFK = s.ServiceID
-- RESTAURAMOS LOS CRUCES DE TIEMPO
LEFT JOIN Time t_admit ON a.AdmitTimeFK = t_admit.TimeID
LEFT JOIN Time t_discharge ON a.DischargeTimeFK = t_discharge.TimeID;
GO