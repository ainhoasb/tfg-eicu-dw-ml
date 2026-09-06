USE [DW_TFG];
GO

CREATE OR ALTER VIEW vw_Dashboard_VitalMeasures AS
SELECT 
    vm.VitalMeasuresID,
    pvm.PatientUnitStayFK AS PatientUnitStayID,
    vm.SpO2,
    vm.HeartRate,
    vm.RespiratoryRate,
    t.Hour AS MeasureHour,
    t.DayNumber AS MeasureDayNumber,
    t.Year AS MeasureYear
FROM VitalMeasures vm
INNER JOIN Patient_VMFact pvm ON vm.VitalMeasuresID = pvm.VitalMeasuresFK
LEFT JOIN Time t ON vm.VMOffset = t.TimeID;
GO