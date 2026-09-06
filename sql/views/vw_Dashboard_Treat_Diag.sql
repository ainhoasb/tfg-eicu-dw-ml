USE [DW_TFG];
GO

-- ==========================================
-- VISTA 1: TRATAMIENTOS EVOLUTIVOS
-- ==========================================
CREATE OR ALTER VIEW vw_Dashboard_Treatments AS
SELECT 
    a.PatientUnitStayFK AS PatientUnitStayID, -- ID para Streamlit
    t.Treatment,                              -- Texto del tratamiento
    ts.Subtype AS TreatmentSubtype,           -- Subcategoría del tratamiento
    s.Service AS TreatmentService             -- Servicio que lo aplica
FROM Treat_AdmFact taf
INNER JOIN Treatment t ON taf.TreatmentFK = t.TreatmentID
INNER JOIN TreatSubtype ts ON t.TreatSubtypeFK = ts.TreatSubID
LEFT JOIN Service s ON ts.TreatServiceFK = s.ServiceID
INNER JOIN AdmittedToICU a ON taf.AdmittedToICUFK = a.AdmICUID;
GO

-- ==========================================
-- VISTA 2: DIAGNÓSTICOS EVOLUTIVOS
-- ==========================================
CREATE OR ALTER VIEW vw_Dashboard_Diagnoses AS
SELECT 
    a.PatientUnitStayFK AS PatientUnitStayID, -- ID para Streamlit
    d.Diagnosis,                              -- Texto del diagnóstico
    ds.Subtype AS DiagnosisSubtype,           -- Subcategoría del diagnóstico
    s.Service AS DiagnosisService             -- Servicio que lo diagnostica
FROM Diag_AdmFact daf
INNER JOIN Diagnosis d ON daf.DiagnosisFK = d.DiagnosisID
INNER JOIN DiagSubtype ds ON d.DiagSubtypeFK = ds.DiagSubID
LEFT JOIN Service s ON ds.DiagServiceFK = s.ServiceID
INNER JOIN AdmittedToICU a ON daf.AdmittedToICUFK = a.AdmICUID;
GO