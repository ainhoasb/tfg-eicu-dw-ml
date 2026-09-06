USE [DW_TFG];
GO

CREATE OR ALTER VIEW vw_Dashboard_AdmittedToICU AS
SELECT 
    -- 1. Identificadores principales (Hechos)
    a.AdmICUID,
    pus.PatientUnitStayID,
    
    -- 2. Dimensión Paciente / Demografía
    p.Gender,
    p.Ethnicity,
    a.Age,
    a.AdmissionHeight,
    a.AdmissionWeight,
    a.DischargeWeight,
    
    -- 3. Dimensión Espacial / Jerarquía para el Treemap
    r.Name AS Region,
    CAST(h.HospitalID AS VARCHAR(10)) AS HospitalID,
    CAST(w.WardID AS VARCHAR(10)) AS WardID,
    u.Type AS UnitType,
    u.StayType AS UnitStayType,
    
    -- 4. Dimensión Diagnóstico de Admisión
    ad.ApacheAdmissionDx AS DiagnosisAdmission,
    s.Service AS Service,
    
    -- 5. Variables Fisiológicas al Ingreso y Scores Clínicos (Tabla AdmittedToICU)
    a.APS,
    a.ApacheScore,
    a.HeartRate AS HeartRate_Admission,
    a.MeanBP AS MeanBP_Admission,
    a.Temperature,
    a.RespiratoryRate AS RespiratoryRate_Admission,
    
    -- 6. Indicadores Clínicos / Flags (0 o 1)
    a.DiedInHospital,
    a.Intubated,
    a.Vent,
    a.Dialysis,
    a.ActiveTreatment,
    a.ElectiveSurgery,
    
    -- 7. Comorbilidades
    a.Diabetes,
    a.Cirrhosis,
    a.HepaticFailure,
    a.MetastaticCancer,
    a.Leukemia,
    a.Lymphoma,
    a.Immunosuppression,
    a.MI,
    
    -- 8. Dimensión Tiempo (Ingreso - Rol 1)
    t_admit.Year AS AdmitYear,
    t_admit.DayNumber AS AdmitDayNumber,
    t_admit.Hour AS AdmitHour,

    -- 9. Dimensión Tiempo (Alta - Rol 2)
    t_discharge.Year AS DischargeYear,
    t_discharge.DayNumber AS DischargeDayNumber,
    t_discharge.Hour AS DischargeHour

FROM AdmittedToICU a
LEFT JOIN PatientUnitStay pus ON a.PatientUnitStayFK = pus.PatientUnitStayID
LEFT JOIN PatientHealthSystem phs ON pus.PatientHealthSystemFK = phs.PatientHealthSystemID
LEFT JOIN Patient p ON phs.PatientFK = p.PatientID
LEFT JOIN Ward w ON a.WardFK = w.WardID
LEFT JOIN Hospital h ON w.HospitalFK = h.HospitalID
LEFT JOIN Region r ON h.RegionFK = r.RegionID
LEFT JOIN Unit u ON a.UnitFK = u.UnitID
LEFT JOIN AdmissionDiagnosis ad ON a.AdmDiagFK = ad.AdmDiagID
LEFT JOIN Service s ON ad.ServiceFK = s.ServiceID
LEFT JOIN Time t_admit ON a.AdmitTimeFK = t_admit.TimeID
LEFT JOIN Time t_discharge ON a.DischargeTimeFK = t_discharge.TimeID;
GO