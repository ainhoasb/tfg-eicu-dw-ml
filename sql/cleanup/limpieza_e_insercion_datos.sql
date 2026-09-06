USE [eICU Collaborative Research Database];
GO

-- Consulta para cambiar valores vacíos a NULL -- Tabla Hospital
UPDATE [dbo].[Temporal_Hospital]
SET 
    hospitalid = NULLIF(hospitalid, ''),
    numbedscategory = NULLIF(numbedscategory, ''),
    teachingstatus = NULLIF(teachingstatus, ''),
    region = NULLIF(region, '');

-- Consulta para insertar datos nuevos -- Tabla Hospital

INSERT INTO [dbo].[Hospital] (HospitalID, NumBedsCategory, TeachingStatus, Region)
SELECT 
    CAST(hospitalid AS INT), 
    numbedscategory,
    teachingstatus,
    region
FROM [dbo].[Temporal_Hospital]
WHERE hospitalid IS NOT NULL -- Evitamos errores con filas vacías
  AND NOT EXISTS (
    SELECT 1 
    FROM [dbo].[Hospital] AS R 
    WHERE R.HospitalID = CAST([dbo].[Temporal_Hospital].hospitalid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla Patient
UPDATE [dbo].[Temporal_Patient]
SET 
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    patienthealthsystemstayid = NULLIF(LTRIM(RTRIM(patienthealthsystemstayid)), ''),
    gender = NULLIF(LTRIM(RTRIM(gender)), ''),
    age = NULLIF(LTRIM(RTRIM(age)), ''),
    ethnicity = NULLIF(LTRIM(RTRIM(ethnicity)), ''),
    hospitalid = NULLIF(LTRIM(RTRIM(hospitalid)), ''),
    wardid = NULLIF(LTRIM(RTRIM(wardid)), ''),
    apacheadmissiondx = NULLIF(LTRIM(RTRIM(apacheadmissiondx)), ''),
    admissionheight = NULLIF(LTRIM(RTRIM(admissionheight)), ''),
    hospitaladmittime24 = NULLIF(LTRIM(RTRIM(hospitaladmittime24)), ''),
    hospitaladmitoffset = NULLIF(LTRIM(RTRIM(hospitaladmitoffset)), ''),
    hospitaladmitsource = NULLIF(LTRIM(RTRIM(hospitaladmitsource)), ''),
    hospitaldischargeyear = NULLIF(LTRIM(RTRIM(hospitaldischargeyear)), ''),
    hospitaldischargetime24 = NULLIF(LTRIM(RTRIM(hospitaldischargetime24)), ''),
    hospitaldischargeoffset = NULLIF(LTRIM(RTRIM(hospitaldischargeoffset)), ''),
    hospitaldischargelocation = NULLIF(LTRIM(RTRIM(hospitaldischargelocation)), ''),
    hospitaldischargestatus = NULLIF(LTRIM(RTRIM(hospitaldischargestatus)), ''),
    unittype = NULLIF(LTRIM(RTRIM(unittype)), ''),
    unitadmittime24 = NULLIF(LTRIM(RTRIM(unitadmittime24)), ''),
    unitadmitsource = NULLIF(LTRIM(RTRIM(unitadmitsource)), ''),
    unitvisitnumber = NULLIF(LTRIM(RTRIM(unitvisitnumber)), ''),
    unitstaytype = NULLIF(LTRIM(RTRIM(unitstaytype)), ''),
    admissionweight = NULLIF(LTRIM(RTRIM(admissionweight)), ''),
    dischargeweight = NULLIF(LTRIM(RTRIM(dischargeweight)), ''),
    unitdischargetime24 = NULLIF(LTRIM(RTRIM(unitdischargetime24)), ''),
    unitdischargeoffset = NULLIF(LTRIM(RTRIM(unitdischargeoffset)), ''),
    unitdischargelocation = NULLIF(LTRIM(RTRIM(unitdischargelocation)), ''),
    unitdischargestatus = NULLIF(LTRIM(RTRIM(unitdischargestatus)), ''),
    uniquepid = NULLIF(LTRIM(RTRIM(uniquepid)), '');

-- Consulta para insertar datos nuevos -- Tabla Patient
INSERT INTO [dbo].[Patient] (
    PatientUnitStayID, PatientHealthSystemStayID, Gender, Age, Ethnicity, 
    HospitalID, WardID, ApacheAdmissionDx, AdmissionHeight, HospitalAdmitTime24, 
    HospitalAdmitOffset, HospitalAdmitSource, HospitalDischargeYear, HospitalDischargeTime24, 
    HospitalDischargeOffset, HospitalDischargeLocation, HospitalDischargeStatus, UnitType, 
    UnitAdmitTime24, UnitAdmitSource, UnitVisitNumber, UnitStayType, AdmissionWeight, 
    DischargeWeight, UnitDischargeTime24, UnitDischargeOffset, UnitDischargeLocation, 
    UnitDischargeStatus, UniquePID
)
SELECT 
    CAST(patientunitstayid AS INT),
    CAST(patienthealthsystemstayid AS INT),
    gender,
    age,
    ethnicity,
    CAST(hospitalid AS INT),
    CAST(wardid AS INT),
    apacheadmissiondx,
    TRY_CAST(admissionheight AS NUMERIC(10,2)), -- TRY_CAST es más seguro para decimales
    hospitaladmittime24,
    TRY_CAST(hospitaladmitoffset AS INT),
    hospitaladmitsource,
    TRY_CAST(hospitaldischargeyear AS SMALLINT),
    hospitaldischargetime24,
    TRY_CAST(hospitaldischargeoffset AS INT),
    hospitaldischargelocation,
    hospitaldischargestatus,
    unittype,
    unitadmittime24,
    unitadmitsource,
    TRY_CAST(unitvisitnumber AS INT),
    unitstaytype,
    TRY_CAST(admissionweight AS NUMERIC(10,2)),
    TRY_CAST(dischargeweight AS NUMERIC(10,2)),
    unitdischargetime24,
    TRY_CAST(unitdischargeoffset AS INT),
    unitdischargelocation,
    unitdischargestatus,
    uniquepid
FROM [dbo].[Temporal_Patient]
WHERE patientunitstayid IS NOT NULL -- No insertamos filas sin ID
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[Patient] 
    WHERE [dbo].[Patient].PatientUnitStayID = CAST([dbo].[Temporal_Patient].patientunitstayid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla CustomLab
UPDATE [dbo].[Temporal_CustomLab]
SET 
    customlabid = NULLIF(LTRIM(RTRIM(customlabid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    labotheroffset = NULLIF(LTRIM(RTRIM(labotheroffset)), ''),
    labothertypeid = NULLIF(LTRIM(RTRIM(labothertypeid)), ''),
    labothername = NULLIF(LTRIM(RTRIM(labothername)), ''),
    labotherresult = NULLIF(LTRIM(RTRIM(labotherresult)), ''),
    labothervaluetext = NULLIF(LTRIM(RTRIM(labothervaluetext)), '');

-- Consulta para insertar datos nuevos -- Tabla CustomLab
INSERT INTO [dbo].[CustomLab] (CustomLabID, PatientUnitStayId, LabOtherOffset, LabOtherTypeID, LabOtherName, LabOtherResult, LabOtherValueText)
SELECT 
    CAST(customlabid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(labotheroffset AS INT),
    CAST(labothertypeid AS INT),
    labothername,
    labotherresult,
    labothervaluetext
FROM [dbo].[Temporal_CustomLab]
WHERE customlabid IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[CustomLab] 
    WHERE [dbo].[CustomLab].CustomLabID = CAST([dbo].[Temporal_CustomLab].customlabid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla VitalAperiodic
UPDATE [dbo].[Temporal_VitalAperiodic]
SET 
    vitalaperiodicid = NULLIF(LTRIM(RTRIM(vitalaperiodicid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    observationoffset = NULLIF(LTRIM(RTRIM(observationoffset)), ''),
    noninvasivesystolic = NULLIF(LTRIM(RTRIM(noninvasivesystolic)), ''),
    noninvasivediastolic = NULLIF(LTRIM(RTRIM(noninvasivediastolic)), ''),
    noninvasivemean = NULLIF(LTRIM(RTRIM(noninvasivemean)), ''),
    paop = NULLIF(LTRIM(RTRIM(paop)), ''),
    cardiacoutput = NULLIF(LTRIM(RTRIM(cardiacoutput)), ''),
    cardiacinput = NULLIF(LTRIM(RTRIM(cardiacinput)), ''),
    svr = NULLIF(LTRIM(RTRIM(svr)), ''),
    svri = NULLIF(LTRIM(RTRIM(svri)), ''),
    pvr = NULLIF(LTRIM(RTRIM(pvr)), ''),
    pvri = NULLIF(LTRIM(RTRIM(pvri)), '');

-- Consulta para insertar datos nuevos -- Tabla VitalAperiodic
INSERT INTO [dbo].[VitalAperiodic] (
    VitalAperiodicID, PatientUnitStayID, ObservationOffset, NonInvasiveSystolic, 
    NonInvasiveDiastolic, NonInvasiveMean, PAOP, CardiacOutput, CardiacInput, 
    SVR, SVRI, PVR, PVRI
)
SELECT 
    CAST(vitalaperiodicid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(observationoffset AS INT),
    CAST(noninvasivesystolic AS FLOAT),
    CAST(noninvasivediastolic AS FLOAT),
    CAST(noninvasivemean AS FLOAT),
    CAST(paop AS FLOAT),
    CAST(cardiacoutput AS FLOAT),
    CAST(cardiacinput AS FLOAT),
    CAST(svr AS FLOAT),
    CAST(svri AS FLOAT),
    CAST(pvr AS FLOAT),
    CAST(pvri AS FLOAT)
FROM [dbo].[Temporal_VitalAperiodic]
WHERE vitalaperiodicid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[VitalAperiodic] 
    WHERE [dbo].[VitalAperiodic].VitalAperiodicID = CAST([dbo].[Temporal_VitalAperiodic].vitalaperiodicid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla VitalPeriodic
UPDATE [dbo].[Temporal_VitalPeriodic]
SET 
    vitalperiodicid = NULLIF(LTRIM(RTRIM(vitalperiodicid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    observationoffset = NULLIF(LTRIM(RTRIM(observationoffset)), ''),
    temperature = NULLIF(LTRIM(RTRIM(temperature)), ''),
    sao2 = NULLIF(LTRIM(RTRIM(sao2)), ''),
    heartrate = NULLIF(LTRIM(RTRIM(heartrate)), ''),
    respiration = NULLIF(LTRIM(RTRIM(respiration)), ''),
    cvp = NULLIF(LTRIM(RTRIM(cvp)), ''),
    etco2 = NULLIF(LTRIM(RTRIM(etco2)), ''),
    systemicsystolic = NULLIF(LTRIM(RTRIM(systemicsystolic)), ''),
    systemicdiastolic = NULLIF(LTRIM(RTRIM(systemicdiastolic)), ''),
    systemicmean = NULLIF(LTRIM(RTRIM(systemicmean)), ''),
    pasystolic = NULLIF(LTRIM(RTRIM(pasystolic)), ''),
    padiastolic = NULLIF(LTRIM(RTRIM(padiastolic)), ''),
    pamean = NULLIF(LTRIM(RTRIM(pamean)), ''),
    st1 = NULLIF(LTRIM(RTRIM(st1)), ''),
    st2 = NULLIF(LTRIM(RTRIM(st2)), ''),
    st3 = NULLIF(LTRIM(RTRIM(st3)), ''),
    icp = NULLIF(LTRIM(RTRIM(icp)), '');

-- Consulta para insertar datos nuevos -- Tabla VitalPeriodic
INSERT INTO [dbo].[VitalPeriodic] (
    VitalPeriodicID, PatientUnitStayID, ObservationOffset, Temperature, 
    saO2, HeartRate, Respiration, CVP, ETCo2, SystemicSystolic, 
    SystemicDiastolic, SystemicMean, paSystolic, paDiastolic, paMean, 
    st1, st2, st3, ICP
)
SELECT 
    CAST(vitalperiodicid AS BIGINT),
    CAST(patientunitstayid AS INT),
    CAST(observationoffset AS INT),
    CAST(temperature AS NUMERIC(11,4)),
    CAST(sao2 AS INT),
    CAST(heartrate AS INT),
    CAST(respiration AS INT),
    CAST(cvp AS INT),
    CAST(etco2 AS INT),
    CAST(systemicsystolic AS INT),
    CAST(systemicdiastolic AS INT),
    CAST(systemicmean AS INT),
    CAST(pasystolic AS INT),
    CAST(padiastolic AS INT),
    CAST(pamean AS INT),
    CAST(st1 AS FLOAT),
    CAST(st2 AS FLOAT),
    CAST(st3 AS FLOAT),
    CAST(icp AS INT)
FROM [dbo].[Temporal_VitalPeriodic]
WHERE vitalperiodicid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[VitalPeriodic] 
    WHERE [dbo].[VitalPeriodic].VitalPeriodicID = CAST([dbo].[Temporal_VitalPeriodic].vitalperiodicid AS BIGINT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla Lab
UPDATE [dbo].[Temporal_Lab]
SET 
    labid = NULLIF(LTRIM(RTRIM(labid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    labresultoffset = NULLIF(LTRIM(RTRIM(labresultoffset)), ''),
    labtypeid = NULLIF(LTRIM(RTRIM(labtypeid)), ''),
    labname = NULLIF(LTRIM(RTRIM(labname)), ''),
    labresult = NULLIF(LTRIM(RTRIM(labresult)), ''),
    labresulttext = NULLIF(LTRIM(RTRIM(labresulttext)), ''),
    labmeasurenamesystem = NULLIF(LTRIM(RTRIM(labmeasurenamesystem)), ''),
    labmeasurenameinterface = NULLIF(LTRIM(RTRIM(labmeasurenameinterface)), ''),
    labresultrevisedoffset = NULLIF(LTRIM(RTRIM(labresultrevisedoffset)), '');

-- Consulta para insertar datos nuevos -- Tabla Lab
INSERT INTO [dbo].[Lab] (
    LabID, PatientUnitStayID, LabResultOffset, LabTypeID, 
    LabName, LabResult, LabResultText, LabMeasureNameSystem, 
    LabMeasureNameInterface, LabResultRevisedOffset
)
SELECT 
    CAST(labid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(labresultoffset AS INT),
    CAST(labtypeid AS NUMERIC(3,0)),
    labname,
    CAST(labresult AS NUMERIC(11,4)),
    labresulttext,
    labmeasurenamesystem,
    labmeasurenameinterface,
    CAST(labresultrevisedoffset AS INT)
FROM [dbo].[Temporal_Lab]
WHERE labid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[Lab] 
    WHERE [dbo].[Lab].LabID = CAST([dbo].[Temporal_Lab].labid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla Allergy
UPDATE [dbo].[Temporal_Allergy]
SET 
    allergyid = NULLIF(LTRIM(RTRIM(allergyid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    allergyoffset = NULLIF(LTRIM(RTRIM(allergyoffset)), ''),
    allergyenteredoffset = NULLIF(LTRIM(RTRIM(allergyenteredoffset)), ''),
    allergynotetype = NULLIF(LTRIM(RTRIM(allergynotetype)), ''),
    specialtytype = NULLIF(LTRIM(RTRIM(specialtytype)), ''),
    usertype = NULLIF(LTRIM(RTRIM(usertype)), ''),
    rxincluded = NULLIF(LTRIM(RTRIM(rxincluded)), ''),
    writtenineicu = NULLIF(LTRIM(RTRIM(writtenineicu)), ''),
    drugname = NULLIF(LTRIM(RTRIM(drugname)), ''),
    allergytype = NULLIF(LTRIM(RTRIM(allergytype)), ''),
    allergyname = NULLIF(LTRIM(RTRIM(allergyname)), ''),
    drughiclseqno = NULLIF(LTRIM(RTRIM(drughiclseqno)), '');

-- Consulta para insertar datos nuevos -- Tabla Allergy
INSERT INTO [dbo].[Allergy] (
    AllergyID, PatientUnitStayID, AllergyOffset, AllergyEnteredOffset, 
    AllergyNoteType, SpecialtyType, UserType, RxIncluded, 
    WrittenIneICU, DrugName, AllergyType, AllergyName, DrugHiclSeqno
)
SELECT 
    CAST(allergyid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(allergyoffset AS INT),
    CAST(allergyenteredoffset AS INT),
    allergynotetype,
    specialtytype,
    usertype,
    rxincluded,
    writtenineicu, -- Mapeado a la columna WrittenInICU de la tabla real
    drugname,
    allergytype,
    allergyname,
    CAST(drughiclseqno AS INT)
FROM [dbo].[Temporal_Allergy]
WHERE allergyid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[Allergy] 
    WHERE [dbo].[Allergy].AllergyID = CAST([dbo].[Temporal_Allergy].allergyid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla ApacheApsVar
UPDATE [dbo].[Temporal_ApacheApsVar]
SET 
    apacheapsvarid = NULLIF(LTRIM(RTRIM(apacheapsvarid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    intubated = NULLIF(LTRIM(RTRIM(intubated)), ''),
    vent = NULLIF(LTRIM(RTRIM(vent)), ''),
    dialysis = NULLIF(LTRIM(RTRIM(dialysis)), ''),
    eyes = NULLIF(LTRIM(RTRIM(eyes)), ''),
    motor = NULLIF(LTRIM(RTRIM(motor)), ''),
    verbal = NULLIF(LTRIM(RTRIM(verbal)), ''),
    meds = NULLIF(LTRIM(RTRIM(meds)), ''),
    urine = NULLIF(LTRIM(RTRIM(urine)), ''),
    wbc = NULLIF(LTRIM(RTRIM(wbc)), ''),
    temperature = NULLIF(LTRIM(RTRIM(temperature)), ''),
    respiratoryrate = NULLIF(LTRIM(RTRIM(respiratoryrate)), ''),
    sodium = NULLIF(LTRIM(RTRIM(sodium)), ''),
    heartrate = NULLIF(LTRIM(RTRIM(heartrate)), ''),
    meanbp = NULLIF(LTRIM(RTRIM(meanbp)), ''),
    ph = NULLIF(LTRIM(RTRIM(ph)), ''),
    hematocrit = NULLIF(LTRIM(RTRIM(hematocrit)), ''),
    creatinine = NULLIF(LTRIM(RTRIM(creatinine)), ''),
    albumin = NULLIF(LTRIM(RTRIM(albumin)), ''),
    pao2 = NULLIF(LTRIM(RTRIM(pao2)), ''),
    pco2 = NULLIF(LTRIM(RTRIM(pco2)), ''),
    bun = NULLIF(LTRIM(RTRIM(bun)), ''),
    glucose = NULLIF(LTRIM(RTRIM(glucose)), ''),
    bilirubin = NULLIF(LTRIM(RTRIM(bilirubin)), ''),
    fio2 = NULLIF(LTRIM(RTRIM(fio2)), '');

-- Consulta para insertar datos nuevos -- Tabla ApacheApsVar
INSERT INTO [dbo].[ApacheApsVar] (
    ApacheApsVarID, PatientUnitStayID, Intubated, Vent, Dialysis, 
    Eyes, Motor, Verbal, Meds, Urine, WBC, Temperature, 
    RespiratoryRate, Sodium, HeartRate, MeanBP, pH, Hematocrit, 
    Creatinine, Albumin, paO2, pCO2, BUN, Glucose, Bilirubin, FiO2
)
SELECT 
    CAST(apacheapsvarid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(intubated AS SMALLINT),
    CAST(vent AS SMALLINT),
    CAST(dialysis AS SMALLINT),
    CAST(eyes AS SMALLINT),
    CAST(motor AS SMALLINT),
    CAST(verbal AS SMALLINT),
    CAST(meds AS SMALLINT),
    TRY_CAST(urine AS FLOAT),
    TRY_CAST(wbc AS FLOAT),
    TRY_CAST(temperature AS FLOAT),
    TRY_CAST(respiratoryrate AS FLOAT),
    TRY_CAST(sodium AS FLOAT),
    TRY_CAST(heartrate AS FLOAT),
    TRY_CAST(meanbp AS FLOAT),
    TRY_CAST(ph AS FLOAT),
    TRY_CAST(hematocrit AS FLOAT),
    TRY_CAST(creatinine AS FLOAT),
    TRY_CAST(albumin AS FLOAT),
    TRY_CAST(pao2 AS FLOAT),
    TRY_CAST(pco2 AS FLOAT),
    TRY_CAST(bun AS FLOAT),
    TRY_CAST(glucose AS FLOAT),
    TRY_CAST(bilirubin AS FLOAT),
    TRY_CAST(fio2 AS FLOAT)
FROM [dbo].[Temporal_ApacheApsVar]
WHERE apacheapsvarid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[ApacheApsVar] 
    WHERE [dbo].[ApacheApsVar].ApacheApsVarID = CAST([dbo].[Temporal_ApacheApsVar].apacheapsvarid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla ApachePredVar
UPDATE [dbo].[Temporal_ApachePredVar]
SET 
    apachepredvarid = NULLIF(LTRIM(RTRIM(apachepredvarid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    sicuday = NULLIF(LTRIM(RTRIM(sicuday)), ''),
    saps3day1 = NULLIF(LTRIM(RTRIM(saps3day1)), ''),
    saps3today = NULLIF(LTRIM(RTRIM(saps3today)), ''),
    saps3yesterday = NULLIF(LTRIM(RTRIM(saps3yesterday)), ''),
    gender = NULLIF(LTRIM(RTRIM(gender)), ''),
    teachtype = NULLIF(LTRIM(RTRIM(teachtype)), ''),
    region = NULLIF(LTRIM(RTRIM(region)), ''),
    bedcount = NULLIF(LTRIM(RTRIM(bedcount)), ''),
    admitsource = NULLIF(LTRIM(RTRIM(admitsource)), ''),
    graftcount = NULLIF(LTRIM(RTRIM(graftcount)), ''),
    meds = NULLIF(LTRIM(RTRIM(meds)), ''),
    verbal = NULLIF(LTRIM(RTRIM(verbal)), ''),
    motor = NULLIF(LTRIM(RTRIM(motor)), ''),
    eyes = NULLIF(LTRIM(RTRIM(eyes)), ''),
    age = NULLIF(LTRIM(RTRIM(age)), ''),
    admitdiagnosis = NULLIF(LTRIM(RTRIM(admitdiagnosis)), ''),
    thrombolytics = NULLIF(LTRIM(RTRIM(thrombolytics)), ''),
    diedinhospital = NULLIF(LTRIM(RTRIM(diedinhospital)), ''),
    aids = NULLIF(LTRIM(RTRIM(aids)), ''),
    hepaticfailure = NULLIF(LTRIM(RTRIM(hepaticfailure)), ''),
    lymphoma = NULLIF(LTRIM(RTRIM(lymphoma)), ''),
    metastaticcancer = NULLIF(LTRIM(RTRIM(metastaticcancer)), ''),
    leukemia = NULLIF(LTRIM(RTRIM(leukemia)), ''),
    immunosuppression = NULLIF(LTRIM(RTRIM(immunosuppression)), ''),
    cirrhosis = NULLIF(LTRIM(RTRIM(cirrhosis)), ''),
    electivesurgery = NULLIF(LTRIM(RTRIM(electivesurgery)), ''),
    activetx = NULLIF(LTRIM(RTRIM(activetx)), ''),
    readmit = NULLIF(LTRIM(RTRIM(readmit)), ''),
    ima = NULLIF(LTRIM(RTRIM(ima)), ''),
    midur = NULLIF(LTRIM(RTRIM(midur)), ''),
    ventday1 = NULLIF(LTRIM(RTRIM(ventday1)), ''),
    oobventday1 = NULLIF(LTRIM(RTRIM(oobventday1)), ''),
    oobintubday1 = NULLIF(LTRIM(RTRIM(oobintubday1)), ''),
    diabetes = NULLIF(LTRIM(RTRIM(diabetes)), ''),
    managementsystem = NULLIF(LTRIM(RTRIM(managementsystem)), ''),
    var03hspxlos = NULLIF(LTRIM(RTRIM(var03hspxlos)), ''),
    pao2 = NULLIF(LTRIM(RTRIM(pao2)), ''),
    fio2 = NULLIF(LTRIM(RTRIM(fio2)), ''),
    ejectfx = NULLIF(LTRIM(RTRIM(ejectfx)), ''),
    creatinine = NULLIF(LTRIM(RTRIM(creatinine)), ''),
    dischargelocation = NULLIF(LTRIM(RTRIM(dischargelocation)), ''),
    visitnumber = NULLIF(LTRIM(RTRIM(visitnumber)), ''),
    amilocation = NULLIF(LTRIM(RTRIM(amilocation)), ''),
    day1meds = NULLIF(LTRIM(RTRIM(day1meds)), ''),
    day1verbal = NULLIF(LTRIM(RTRIM(day1verbal)), ''),
    day1motor = NULLIF(LTRIM(RTRIM(day1motor)), ''),
    day1eyes = NULLIF(LTRIM(RTRIM(day1eyes)), ''),
    day1pao2 = NULLIF(LTRIM(RTRIM(day1pao2)), ''),
    day1fio2 = NULLIF(LTRIM(RTRIM(day1fio2)), '');

-- Consulta para insertar datos nuevos -- Tabla ApachePredVar
INSERT INTO [dbo].[ApachePredVar] (
    ApachePredVarID, PatientUnitStayID, SicuDay, Saps3Day1, Saps3Today, 
    Saps3Yesterday, Gender, TeachType, Region, BedCount, AdmitSource, 
    GraftCount, Meds, Verbal, Motor, Eyes, Age, AdmitDiagnosis, 
    Thrombolytics, DiedInHospital, Aids, HepaticFailure, Lymphoma, 
    MetastaticCancer, Leukemia, Immunosuppression, Cirrhosis, ElectiveSurgery, 
    ActiveTx, Readmit, Ima, MIDur, VentDay1, oOBVentDay1, oOBIntubDay1, 
    Diabetes, ManagementSystem, var03HspXlos, paO2, fiO2, EjectFx, 
    Creatinine, DischargeLocation, VisitNumber, AMILocation, Day1Meds, 
    Day1Verbal, Day1Motor, Day1Eyes, Day1paO2, Day1fiO2
)
SELECT 
    CAST(apachepredvarid AS INT),
    CAST(patientunitstayid AS INT),
    TRY_CAST(sicuday AS SMALLINT),
    TRY_CAST(saps3day1 AS SMALLINT),
    TRY_CAST(saps3today AS SMALLINT),
    TRY_CAST(saps3yesterday AS SMALLINT),
    TRY_CAST(gender AS SMALLINT),
    TRY_CAST(teachtype AS SMALLINT),
    TRY_CAST(region AS SMALLINT),
    TRY_CAST(bedcount AS SMALLINT),
    TRY_CAST(admitsource AS SMALLINT),
    TRY_CAST(graftcount AS SMALLINT),
    TRY_CAST(meds AS SMALLINT),
    TRY_CAST(verbal AS SMALLINT),
    TRY_CAST(motor AS SMALLINT),
    TRY_CAST(eyes AS SMALLINT),
    TRY_CAST(age AS SMALLINT),
    admitdiagnosis,
    TRY_CAST(thrombolytics AS SMALLINT),
    TRY_CAST(diedinhospital AS SMALLINT),
    TRY_CAST(aids AS SMALLINT),
    TRY_CAST(hepaticfailure AS SMALLINT),
    TRY_CAST(lymphoma AS SMALLINT),
    TRY_CAST(metastaticcancer AS SMALLINT),
    TRY_CAST(leukemia AS SMALLINT),
    TRY_CAST(immunosuppression AS SMALLINT),
    TRY_CAST(cirrhosis AS SMALLINT),
    TRY_CAST(electivesurgery AS SMALLINT),
    TRY_CAST(activetx AS SMALLINT),
    TRY_CAST(readmit AS SMALLINT),
    TRY_CAST(ima AS SMALLINT),
    TRY_CAST(midur AS SMALLINT),
    TRY_CAST(ventday1 AS SMALLINT),
    TRY_CAST(oobventday1 AS SMALLINT),
    TRY_CAST(oobintubday1 AS SMALLINT),
    TRY_CAST(diabetes AS SMALLINT),
    TRY_CAST(managementsystem AS SMALLINT),
    TRY_CAST(var03hspxlos AS FLOAT),
    TRY_CAST(pao2 AS FLOAT),
    TRY_CAST(fio2 AS FLOAT),
    TRY_CAST(ejectfx AS FLOAT),
    TRY_CAST(creatinine AS FLOAT),
    TRY_CAST(dischargelocation AS SMALLINT),
    TRY_CAST(visitnumber AS SMALLINT),
    TRY_CAST(amilocation AS SMALLINT),
    TRY_CAST(day1meds AS SMALLINT),
    TRY_CAST(day1verbal AS SMALLINT),
    TRY_CAST(day1motor AS SMALLINT),
    TRY_CAST(day1eyes AS SMALLINT),
    TRY_CAST(day1pao2 AS FLOAT),
    TRY_CAST(day1fio2 AS FLOAT)
FROM [dbo].[Temporal_ApachePredVar]
WHERE apachepredvarid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[ApachePredVar] 
    WHERE [dbo].[ApachePredVar].ApachePredVarID = CAST([dbo].[Temporal_ApachePredVar].apachepredvarid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla ApachePatientResult
UPDATE [dbo].[Temporal_ApachePatientResult]
SET 
    apachepatientresultsid = NULLIF(LTRIM(RTRIM(apachepatientresultsid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    physicianspeciality = NULLIF(LTRIM(RTRIM(physicianspeciality)), ''),
    physicianinterventioncategory = NULLIF(LTRIM(RTRIM(physicianinterventioncategory)), ''),
    acutephysiologyscore = NULLIF(LTRIM(RTRIM(acutephysiologyscore)), ''),
    apachescore = NULLIF(LTRIM(RTRIM(apachescore)), ''),
    apacheversion = NULLIF(LTRIM(RTRIM(apacheversion)), ''),
    predictedicumortality = NULLIF(LTRIM(RTRIM(predictedicumortality)), ''),
    actualicumortality = NULLIF(LTRIM(RTRIM(actualicumortality)), ''),
    predictediculos = NULLIF(LTRIM(RTRIM(predictediculos)), ''),
    actualiculos = NULLIF(LTRIM(RTRIM(actualiculos)), ''),
    predictedhospitalmortality = NULLIF(LTRIM(RTRIM(predictedhospitalmortality)), ''),
    actualhospitalmortality = NULLIF(LTRIM(RTRIM(actualhospitalmortality)), ''),
    predictedhospitallos = NULLIF(LTRIM(RTRIM(predictedhospitallos)), ''),
    actualhospitallos = NULLIF(LTRIM(RTRIM(actualhospitallos)), ''),
    preopmi = NULLIF(LTRIM(RTRIM(preopmi)), ''),
    preopcardiaccath = NULLIF(LTRIM(RTRIM(preopcardiaccath)), ''),
    ptcawithin24h = NULLIF(LTRIM(RTRIM(ptcawithin24h)), ''),
    unabridgedunitlos = NULLIF(LTRIM(RTRIM(unabridgedunitlos)), ''),
    unabridgedhosplos = NULLIF(LTRIM(RTRIM(unabridgedhosplos)), ''),
    actualventdays = NULLIF(LTRIM(RTRIM(actualventdays)), ''),
    predventdays = NULLIF(LTRIM(RTRIM(predventdays)), ''),
    unabridgedactualventdays = NULLIF(LTRIM(RTRIM(unabridgedactualventdays)), '');

-- Consulta para insertar datos nuevos -- Tabla ApachePatientResult
INSERT INTO [dbo].[ApachePatientResult] (
    ApachePatientResultsID, PatientUnitStayID, PhysicianSpeciality, 
    PhysicianInterventionCategory, AcutePhysiologyScore, ApacheScore, 
    ApacheVersion, PredictedICUMortality, ActualICUMortality, 
    PredictedICULOS, ActualICULOS, PredictedHospitalMortality, 
    ActualHospitalMortality, PredictedHospitalLOS, ActualHospitalLOS, 
    PreopMI, PreopCardiacCath, PTCAwithin24h, UnabridgedUnitLOS, 
    UnabridgedHospLOS, ActualVentDays, PredVentDays, UnabridgedActualVentDays
)
SELECT 
    CAST(apachepatientresultsid AS INT),
    CAST(patientunitstayid AS INT),
    physicianspeciality,
    physicianinterventioncategory,
    TRY_CAST(acutephysiologyscore AS INT),
    TRY_CAST(apachescore AS INT),
    apacheversion,
    predictedicumortality,
    actualicumortality,
    TRY_CAST(predictediculos AS FLOAT),
    TRY_CAST(actualiculos AS FLOAT),
    predictedhospitalmortality,
    actualhospitalmortality,
    TRY_CAST(predictedhospitallos AS FLOAT),
    TRY_CAST(actualhospitallos AS FLOAT),
    TRY_CAST(preopmi AS INT),
    TRY_CAST(preopcardiaccath AS INT),
    TRY_CAST(ptcawithin24h AS INT),
    TRY_CAST(unabridgedunitlos AS FLOAT),
    TRY_CAST(unabridgedhosplos AS FLOAT),
    TRY_CAST(actualventdays AS FLOAT),
    TRY_CAST(predventdays AS FLOAT),
    TRY_CAST(unabridgedactualventdays AS FLOAT)
FROM [dbo].[Temporal_ApachePatientResult]
WHERE apachepatientresultsid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[ApachePatientResult] 
    WHERE [dbo].[ApachePatientResult].ApachePatientResultsID = CAST([dbo].[Temporal_ApachePatientResult].apachepatientresultsid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla PhysicalExam
UPDATE [dbo].[Temporal_PhysicalExam]
SET 
    physicalexamid = NULLIF(LTRIM(RTRIM(physicalexamid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    physicalexamoffset = NULLIF(LTRIM(RTRIM(physicalexamoffset)), ''),
    physicalexampath = NULLIF(LTRIM(RTRIM(physicalexampath)), ''),
    physicalexamvalue = NULLIF(LTRIM(RTRIM(physicalexamvalue)), ''),
    physicalexamtext = NULLIF(LTRIM(RTRIM(physicalexamtext)), '');

-- Consulta para insertar datos nuevos -- Tabla PhysicalExam
INSERT INTO [dbo].[PhysicalExam] (
    PhysicalExamID, PatientUnitStayID, PhysicalExamOffset, 
    PhysicalExamPath, PhysicalExamValue, PhysicalExamText
)
SELECT 
    CAST(physicalexamid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(physicalexamoffset AS INT),
    physicalexampath,
    physicalexamvalue,
    physicalexamtext
FROM [dbo].[Temporal_PhysicalExam]
WHERE physicalexamid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[PhysicalExam] 
    WHERE [dbo].[PhysicalExam].PhysicalExamID = CAST([dbo].[Temporal_PhysicalExam].physicalexamid AS INT)
);

-- Consulta para cambiar valores vacíos a NULL -- Tabla PastHistory
UPDATE [dbo].[Temporal_PastHistory]
SET 
    pasthistoryid = NULLIF(LTRIM(RTRIM(pasthistoryid)), ''),
    patientunitstayid = NULLIF(LTRIM(RTRIM(patientunitstayid)), ''),
    pasthistoryoffset = NULLIF(LTRIM(RTRIM(pasthistoryoffset)), ''),
    pasthistoryenteredoffset = NULLIF(LTRIM(RTRIM(pasthistoryenteredoffset)), ''),
    pasthistorynotetype = NULLIF(LTRIM(RTRIM(pasthistorynotetype)), ''),
    pasthistorypath = NULLIF(LTRIM(RTRIM(pasthistorypath)), ''),
    pasthistoryvalue = NULLIF(LTRIM(RTRIM(pasthistoryvalue)), ''),
    pasthistoryvaluetext = NULLIF(LTRIM(RTRIM(pasthistoryvaluetext)), '');

-- Consulta para insertar datos nuevos -- Tabla PastHistory
INSERT INTO [dbo].[PastHistory] (
    PastHistoryID, PatientUnitStayID, PastHistoryOffset, 
    PastHistoryEnteredOffset, PastHistoryNoteType, PastHistoryPath, 
    PastHistoryValue, PastHistoryValueText
)
SELECT 
    CAST(pasthistoryid AS INT),
    CAST(patientunitstayid AS INT),
    CAST(pasthistoryoffset AS INT),
    CAST(pasthistoryenteredoffset AS INT),
    pasthistorynotetype,
    pasthistorypath,
    pasthistoryvalue,
    pasthistoryvaluetext
FROM [dbo].[Temporal_PastHistory]
WHERE pasthistoryid IS NOT NULL 
  AND NOT EXISTS (
    SELECT 1 FROM [dbo].[PastHistory] 
    WHERE [dbo].[PastHistory].PastHistoryID = CAST([dbo].[Temporal_PastHistory].pasthistoryid AS INT)
);