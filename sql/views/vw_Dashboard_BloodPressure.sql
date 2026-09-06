USE [DW_TFG];
GO

CREATE OR ALTER VIEW vw_Dashboard_BloodPressure AS
SELECT 
    bp.BloodPressureID,
    pbp.PatientUnitStayFK AS PatientUnitStayID,
    bp.Systolic,
    bp.Diastolic,
    bp.Mean,
    t.Hour AS MeasureHour,
    t.DayNumber AS MeasureDayNumber,
    t.Year AS MeasureYear
FROM NonInvasiveBloodPressure bp
INNER JOIN Patient_BPFact pbp ON bp.BloodPressureID = pbp.BloodPressureFK
LEFT JOIN Time t ON bp.BPOffset = t.TimeID
WHERE bp.Systolic > 0 
  AND bp.Diastolic > 0;
GO