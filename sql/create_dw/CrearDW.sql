USE [DW_TFG]
GO

-- =============================================
-- 1. CREACIÓN DE TABLAS (DDL BASE)
-- =============================================

CREATE TABLE AdmissionDiagnosis 
    (
     AdmDiagID INT PRIMARY KEY IDENTITY(1,1) , 
     ApacheAdmissionDx VARCHAR (1000) NOT NULL , 
     ServiceFK INT NOT NULL 
    )
GO

CREATE TABLE AdmitLocation 
    (
     AdmitLocID INT PRIMARY KEY IDENTITY(1,1) , 
     Source VARCHAR (30) 
    )
GO

CREATE TABLE AdmittedToICU 
    (
     AdmICUID INT PRIMARY KEY IDENTITY(1,1) , 
     Age NUMERIC (2,0) , 
     AdmissionHeight NUMERIC (10,2) , 
     AdmissionWeight NUMERIC (10,2) , 
     DischargeWeight NUMERIC (10,2) , 
     APS INT , 
     ApacheScore INT , 
     Intubated BIT , 
     Vent BIT , 
     Dialysis BIT , 
     Eyes SMALLINT , 
     Motor SMALLINT , 
     Verbal SMALLINT , 
     Meds BIT , 
     Urine NUMERIC (18,6) , --Modificado respecto al original
     WBC NUMERIC (5,2) , --Modificado respecto al original
     Temperature NUMERIC (4,2) , 
     RespiratoryRate NUMERIC (2,0) , 
     Sodium NUMERIC (4,1) , 
     HeartRate NUMERIC (3,0) , 
     MeanBP NUMERIC (3,0) , 
     pH NUMERIC (4,3) , 
     Hematocrit NUMERIC (3,1) , 
     Creatinine NUMERIC (4,2) , 
     Albumin NUMERIC (2,1) , 
     PaO2 NUMERIC (4,1) , 
     pCO2 NUMERIC (4,1) , 
     BUN NUMERIC (5,2) , 
     Glucose NUMERIC (4,0) , --Modificado respecto al original
     Bilirubin NUMERIC (4,2) , 
     FiO2 NUMERIC (3,0) , 
     DiedInHospital BIT , 
     ActiveTreatment BIT , 
     ElectiveSurgery BIT , 
     Thrombolytics BIT , 
     HepaticFailure BIT , 
     Lymphoma BIT , 
     MetastaticCancer BIT , 
     Leukemia BIT , 
     Immunosuppression BIT , 
     Cirrhosis BIT , 
     IMA BIT , 
     MI BIT , 
     VentApacheDay BIT , 
     IntubApacheDay BIT , 
     Diabetes BIT , 
     EjectionFraction NUMERIC (2,0) , 
     AMILocation SMALLINT , 
     HasPhysicalExam BIT , 
     PastHistory VARCHAR (18) , 
     AdmitTimeFK INT NOT NULL , 
     DischargeTimeFK INT NOT NULL , 
     PatientUnitStayFK INT NOT NULL ,
     WardFK INT NOT NULL , 
     AdmitInUnitFK INT NOT NULL , 
     AdmitInHospitalFK INT NOT NULL , 
     DischargeFromHospitalFK INT NOT NULL , 
     DischargeFromUnitFK INT NOT NULL , 
     UnitFK INT NOT NULL ,
     AdmDiagFK INT NOT NULL
    )
GO

CREATE TABLE Allergy 
    (
     AllergyID INT PRIMARY KEY IDENTITY(1,1) , 
     Name VARCHAR (255) NOT NULL , 
     DrugHiclSeqNo INT , 
     AllergyTypeFK INT NOT NULL 
    )
GO

CREATE TABLE Allergy_AdmFact 
    (
     AllergyFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE Allergy_AdmFact ADD CONSTRAINT Allergy_AdmFact_PK PRIMARY KEY ( AllergyFK, 
                                                                            AdmittedToICUFK );
GO

CREATE TABLE AllergyType 
    (
     AllergyTypeID INT PRIMARY KEY IDENTITY(1,1) , 
     Type VARCHAR (8) NOT NULL 
    )
GO

CREATE TABLE Diag_AdmFact 
    (
     DiagnosisFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE Diag_AdmFact ADD CONSTRAINT Diag_AdmFact_PK PRIMARY KEY ( DiagnosisFK, 
                                                                      AdmittedToICUFK );
GO

CREATE TABLE Diagnosis 
    (
     DiagnosisID INT PRIMARY KEY IDENTITY(1,1) , 
     Diagnosis VARCHAR (70) NOT NULL , 
     MoreInfo VARCHAR (100) , 
     ActiveUponDischarge BIT , 
     DiagSubtypeFK INT NOT NULL 
    )
GO

CREATE TABLE DiagSubtype 
    (
     DiagSubID INT PRIMARY KEY IDENTITY(1,1) , 
     Subtype VARCHAR (70) NOT NULL , 
     DiagServiceFK INT NOT NULL 
    )
GO

CREATE TABLE Discharge
    (
     DischargeID INT PRIMARY KEY IDENTITY(1,1) , 
     Location VARCHAR (100) , 
     Status VARCHAR (10) 
    )
GO

CREATE TABLE Hospital 
    (
     HospitalID INT PRIMARY KEY , 
     RegionFK INT NOT NULL 
    )
GO

CREATE TABLE Lab_AdmFact 
    (
     LabTestFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE Lab_AdmFact ADD CONSTRAINT Lab_AdmFact_PK PRIMARY KEY ( LabTestFK, 
                                                                    AdmittedToICUFK );
GO

CREATE TABLE LabTest 
    (
     LabTestID INT PRIMARY KEY IDENTITY(1,1) , 
     MedicalTest VARCHAR (32) NOT NULL , 
     Result VARCHAR (64) , --Modificado respecto al original
     Measure VARCHAR (20) 
    )
GO

CREATE TABLE NonInvasiveBloodPressure 
    (
     BloodPressureID INT PRIMARY KEY IDENTITY(1,1) , 
     Systolic NUMERIC (3,0) , 
     Diastolic NUMERIC (3,0) , 
     Mean NUMERIC (3,0) , 
     BPOffset INT NOT NULL
    )
GO

CREATE TABLE PastHist_AdmFact 
    (
     PastHistoryFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE PastHist_AdmFact ADD CONSTRAINT PastHist_AdmFact_PK PRIMARY KEY ( PastHistoryFK, 
                                                                              AdmittedToICUFK );
GO

CREATE TABLE PastHistory 
    (
     PastHistoryID INT PRIMARY KEY IDENTITY(1,1) , 
     PastHistory VARCHAR (70) NOT NULL , 
     MoreInfo VARCHAR (100) , 
     PastHistSubtypeFK INT NOT NULL 
    )
GO

CREATE TABLE PastHistSubtype 
    (
     PastHistSubID INT PRIMARY KEY IDENTITY(1,1) , 
     Subtype VARCHAR (70) NOT NULL , 
     PastHistTypeFK INT NOT NULL 
    )
GO

CREATE TABLE PastHistType 
    (
     PastHistTypeID INT PRIMARY KEY IDENTITY(1,1) , 
     Type VARCHAR (25) NOT NULL 
    )
GO

CREATE TABLE Patient 
    (
     PatientID VARCHAR(10) PRIMARY KEY , 
     Gender VARCHAR (25) , 
     Ethnicity VARCHAR (50) 
    )
GO

CREATE TABLE Patient_BPFact 
    (
     BloodPressureFK INT NOT NULL , 
     PatientUnitStayFK INT NOT NULL 
    )
GO

ALTER TABLE Patient_BPFact ADD CONSTRAINT Patient_BPFact_PK PRIMARY KEY (BloodPressureFK,
                                                                         PatientUnitStayFK)
GO

CREATE TABLE Patient_VMFact 
    (
     VitalMeasuresFK INT NOT NULL , 
     PatientUnitStayFK INT NOT NULL 
    )
GO

ALTER TABLE Patient_VMFact ADD CONSTRAINT Patient_VMFact_PK PRIMARY KEY (VitalMeasuresFK,
                                                                         PatientUnitStayFK)
GO

CREATE TABLE PatientHealthSystem 
    (
     PatientHealthSystemID INT PRIMARY KEY , 
     PatientFK VARCHAR(10) NOT NULL 
    )
GO

CREATE TABLE PatientUnitStay 
    (
     PatientUnitStayID INT PRIMARY KEY , 
     PatientHealthSystemFK INT NOT NULL
    )
GO

CREATE TABLE PhyEx_AdmFact 
    (
     PhysicalExamFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE PhyEx_AdmFact ADD CONSTRAINT PhyEx_AdmFact_PK PRIMARY KEY ( PhysicalExamFK, 
                                                                        AdmittedToICUFK );
GO

CREATE TABLE PhyExSubtype 
    (
     PhyExSubID INT PRIMARY KEY IDENTITY(1,1) , 
     Subtype VARCHAR (70) NOT NULL , 
     PhyExTypeFK INT NOT NULL 
    )
GO

CREATE TABLE PhyExType 
    (
     PhyExTypeID INT PRIMARY KEY IDENTITY(1,1) , 
     Type VARCHAR (25) NOT NULL 
    )
GO

CREATE TABLE PhysicalExam 
    (
     PhyExID INT PRIMARY KEY IDENTITY(1,1) , 
     PhysicalExam VARCHAR (70) NOT NULL , 
     MoreInfo VARCHAR (70) , 
     Result VARCHAR (50) , 
     PhyExSubtypeFK INT NOT NULL 
    )
GO

CREATE TABLE Region 
    (
     RegionID INT PRIMARY KEY IDENTITY(1,1) , 
     Name VARCHAR (64) 
    )
GO

CREATE TABLE Service 
    (
     ServiceID INT PRIMARY KEY IDENTITY(1,1) ,
     Service VARCHAR (25) NOT NULL 
    )
GO

CREATE TABLE Time 
    (
     TimeID INT PRIMARY KEY IDENTITY(1,1) , 
     Hour VARCHAR (8) NOT NULL , 
     DayNumber INT NOT NULL , 
     Year VARCHAR (4) NOT NULL 
    )
GO

CREATE TABLE Treat_AdmFact 
    (
     TreatmentFK INT NOT NULL , 
     AdmittedToICUFK INT NOT NULL 
    )
GO

ALTER TABLE Treat_AdmFact ADD CONSTRAINT Treat_AdmFact_PK PRIMARY KEY ( TreatmentFK, 
                                                                        AdmittedToICUFK );
GO

CREATE TABLE Treatment 
    (
     TreatmentID INT PRIMARY KEY IDENTITY(1,1) , 
     Treatment VARCHAR (70) NOT NULL , 
     MoreInfo VARCHAR (100) , 
     ActiveUponDischarge BIT , 
     TreatSubtypeFK INT NOT NULL 
    )
GO

CREATE TABLE TreatSubtype 
    (
     TreatSubID INT PRIMARY KEY IDENTITY(1,1) , 
     Subtype VARCHAR (70) NOT NULL , 
     TreatServiceFK INT NOT NULL 
    )
GO

CREATE TABLE Unit 
    (
     UnitID INT PRIMARY KEY IDENTITY(1,1) , 
     Type VARCHAR (50) NOT NULL , 
     StayType VARCHAR (15) NOT NULL 
    )
GO

CREATE TABLE VitalMeasures 
    (
     VitalMeasuresID INT PRIMARY KEY IDENTITY(1,1) , 
     SpO2 INT , 
     HeartRate INT , 
     RespiratoryRate INT ,
     VMOffset INT NOT NULL
    )
GO

CREATE TABLE Ward 
    (
     WardID INT PRIMARY KEY , 
     HospitalFK INT NOT NULL 
    )
GO

-- =============================================
-- 2. RESTRICCIONES DE CLAVES FORÁNEAS (FK)
-- =============================================

ALTER TABLE AdmissionDiagnosis 
    ADD CONSTRAINT AdmissionDiagnosis_Service_FK FOREIGN KEY ( ServiceFK )
    REFERENCES Service ( ServiceID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_AdmissionDiagnosis_FK FOREIGN KEY ( AdmDiagFK )
    REFERENCES AdmissionDiagnosis ( AdmDiagID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_AdmitInHospital_FK FOREIGN KEY ( AdmitInHospitalFK ) 
    REFERENCES AdmitLocation ( AdmitLocID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_AdmitInUnit_FK FOREIGN KEY ( AdmitInUnitFK ) 
    REFERENCES AdmitLocation ( AdmitLocID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_DischargeFromHospital_FK FOREIGN KEY ( DischargeFromHospitalFK ) 
    REFERENCES Discharge ( DischargeID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_DischargeFromUnit_FK FOREIGN KEY ( DischargeFromUnitFK ) 
    REFERENCES Discharge ( DischargeID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_PatientUnitStay_FK FOREIGN KEY ( PatientUnitStayFK ) 
    REFERENCES PatientUnitStay ( PatientUnitStayID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT DischargeTimeFK FOREIGN KEY ( DischargeTimeFK ) 
    REFERENCES Time ( TimeID ) 
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmitTimeFK FOREIGN KEY ( AdmitTimeFK ) 
    REFERENCES Time ( TimeID )
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_Unit_FK FOREIGN KEY ( UnitFK ) 
    REFERENCES Unit ( UnitID ) 
GO

ALTER TABLE AdmittedToICU 
    ADD CONSTRAINT AdmittedToICU_Ward_FK FOREIGN KEY ( WardFK ) 
    REFERENCES Ward ( WardID )
GO

ALTER TABLE Allergy_AdmFact 
    ADD CONSTRAINT Allergy_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE Allergy_AdmFact 
    ADD CONSTRAINT Allergy_AdmFact_Allergy_FK FOREIGN KEY ( AllergyFK ) 
    REFERENCES Allergy ( AllergyID ) 
GO

ALTER TABLE Allergy 
    ADD CONSTRAINT Allergy_AllergyType_FK FOREIGN KEY ( AllergyTypeFK ) 
    REFERENCES AllergyType ( AllergyTypeID )
GO

ALTER TABLE Diag_AdmFact 
    ADD CONSTRAINT Diag_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE Diag_AdmFact 
    ADD CONSTRAINT Diag_AdmFact_Diagnosis_FK FOREIGN KEY ( DiagnosisFK ) 
    REFERENCES Diagnosis ( DiagnosisID )
GO

ALTER TABLE Diagnosis 
    ADD CONSTRAINT Diagnosis_DiagSubtype_FK FOREIGN KEY ( DiagSubtypeFK ) 
    REFERENCES DiagSubtype ( DiagSubID )
GO

ALTER TABLE DiagSubtype 
    ADD CONSTRAINT DiagSubtype_DiagService_FK FOREIGN KEY ( DiagServiceFK) 
    REFERENCES Service ( ServiceID )
GO

ALTER TABLE Hospital 
    ADD CONSTRAINT Hospital_Region_FK FOREIGN KEY ( RegionFK ) 
    REFERENCES Region ( RegionID )
GO

ALTER TABLE Lab_AdmFact 
    ADD CONSTRAINT Lab_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE Lab_AdmFact 
    ADD CONSTRAINT Lab_AdmFact_LabTest_FK FOREIGN KEY ( LabTestFK ) 
    REFERENCES LabTest ( LabTestID )
GO

ALTER TABLE PastHist_AdmFact 
    ADD CONSTRAINT PastHist_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE PastHist_AdmFact 
    ADD CONSTRAINT PastHist_AdmFact_PastHistory_FK FOREIGN KEY ( PastHistoryFK ) 
    REFERENCES PastHistory ( PastHistoryID )
GO

ALTER TABLE PastHistory 
    ADD CONSTRAINT PastHistory_PastHistSubtype_FK FOREIGN KEY ( PastHistSubtypeFK ) 
    REFERENCES PastHistSubtype ( PastHistSubID )
GO

ALTER TABLE PastHistSubtype 
    ADD CONSTRAINT PastHistSubtype_PastHistType_FK FOREIGN KEY ( PastHistTypeFK ) 
    REFERENCES PastHistType ( PastHistTypeID )
GO

ALTER TABLE PatientHealthSystem 
    ADD CONSTRAINT PatientHealthSystem_Patient_FK FOREIGN KEY ( PatientFK ) 
    REFERENCES Patient ( PatientID )
GO

ALTER TABLE PatientUnitStay 
    ADD CONSTRAINT PatientUnitStay_PatientHealthSystem_FK FOREIGN KEY ( PatientHealthSystemFK ) 
    REFERENCES PatientHealthSystem ( PatientHealthSystemID )
GO

ALTER TABLE PhyEx_AdmFact 
    ADD CONSTRAINT PhyEx_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE PhyEx_AdmFact 
    ADD CONSTRAINT PhyEx_AdmFact_PhysicalExam_FK FOREIGN KEY ( PhysicalExamFK ) 
    REFERENCES PhysicalExam ( PhyExID )
GO

ALTER TABLE PhyExSubtype 
    ADD CONSTRAINT PhyExSubtype_PhyExType_FK FOREIGN KEY ( PhyExTypeFK ) 
    REFERENCES PhyExType ( PhyExTypeID )
GO

ALTER TABLE PhysicalExam 
    ADD CONSTRAINT PhysicalExam_PhyExSubtype_FK FOREIGN KEY ( PhyExSubtypeFK ) 
    REFERENCES PhyExSubtype ( PhyExSubID )
GO

ALTER TABLE Treat_AdmFact 
    ADD CONSTRAINT Treat_AdmFact_AdmittedToICU_FK FOREIGN KEY ( AdmittedToICUFK ) 
    REFERENCES AdmittedToICU ( AdmICUID )
GO

ALTER TABLE Treat_AdmFact 
    ADD CONSTRAINT Treat_AdmFact_Treatment_FK FOREIGN KEY ( TreatmentFK ) 
    REFERENCES Treatment ( TreatmentID )
GO

ALTER TABLE Treatment 
    ADD CONSTRAINT Treatment_TreatSubtype_FK FOREIGN KEY ( TreatSubtypeFK ) 
    REFERENCES TreatSubtype ( TreatSubID )
GO

ALTER TABLE TreatSubtype 
    ADD CONSTRAINT TreatSubtype_TreatService_FK FOREIGN KEY ( TreatServiceFK ) 
    REFERENCES Service ( ServiceID )
GO

ALTER TABLE NonInvasiveBloodPressure 
    ADD CONSTRAINT NonInvasiveBloodPressure_Time_FK FOREIGN KEY ( BPOffset ) 
    REFERENCES Time ( TimeID )
GO

ALTER TABLE VitalMeasures 
    ADD CONSTRAINT VitalMeasures_Time_FK FOREIGN KEY ( VMOffset ) 
    REFERENCES Time ( TimeID )
GO

ALTER TABLE Ward 
    ADD CONSTRAINT Ward_Hospital_FK FOREIGN KEY ( HospitalFK ) 
    REFERENCES Hospital ( HospitalID )
GO

ALTER TABLE Patient_BPFact 
    ADD CONSTRAINT Patient_BPFact_NonInvasiveBloodPressure_FK FOREIGN KEY ( BloodPressureFK ) 
    REFERENCES NonInvasiveBloodPressure ( BloodPressureID )
GO

ALTER TABLE Patient_BPFact 
    ADD CONSTRAINT Patient_BPFact_PatientUnitStay_FK FOREIGN KEY ( PatientUnitStayFK ) 
    REFERENCES PatientUnitStay ( PatientUnitStayID )
GO

ALTER TABLE Patient_VMFact 
    ADD CONSTRAINT Patient_VMFact_PatientUnitStay_FK FOREIGN KEY ( PatientUnitStayFK ) 
    REFERENCES PatientUnitStay ( PatientUnitStayID ) 
GO

ALTER TABLE Patient_VMFact 
    ADD CONSTRAINT Patient_VMFact_VitalMeasures_FK FOREIGN KEY ( VitalMeasuresFK ) 
    REFERENCES VitalMeasures ( VitalMeasuresID )
GO

-- =============================================
-- 3. ÍNDICES ADICIONALES DE OPTIMIZACIÓN
-- =============================================

CREATE NONCLUSTERED INDEX IX_VitalMeasures_BusquedaMasiva
ON [dbo].[VitalMeasures] ([SpO2], [HeartRate], [RespiratoryRate])
INCLUDE ([VitalMeasuresID], [VMOffset]);
GO

CREATE NONCLUSTERED INDEX IX_Time_BusquedaMasiva
ON [dbo].[Time] ([Year], [Hour], [DayNumber])
INCLUDE ([TimeID]);
GO