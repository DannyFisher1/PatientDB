CREATE TABLE IF NOT EXISTS patient_cases (
    case_id TEXT PRIMARY KEY,
    arrival_severity TEXT,
    gender TEXT,
    age INTEGER,
    injury_icd10_1 TEXT,
    injury_icd10_2 TEXT,
    injury_ais_1 INTEGER,
    injury_ais_2 INTEGER,
    combat_status INTEGER,
    max_iss_score INTEGER,
    mechanism_injury TEXT,
    primary_injury_type TEXT,
    secondary_injury_type TEXT,
    tertiary_injury_type TEXT,
    medical_complications TEXT,
    first_bed_type TEXT,
    first_bed_hours INTEGER,
    first_bed_start INTEGER,
    first_bed_end INTEGER,
    second_bed_type TEXT,
    second_bed_hours INTEGER,
    second_bed_start INTEGER,
    second_bed_end INTEGER,
    post_acute_bed_type TEXT,
    post_acute_bed_hours INTEGER,
    post_acute_bed_start INTEGER,
    post_acute_bed_end INTEGER,
    disposition TEXT,
    primary_specialty TEXT,
    secondary_specialty TEXT,
    tertiary_specialty TEXT,
    other_specialty_resource_1 TEXT,
    other_specialty_resource_2 TEXT,
    other_specialty_resource_3 TEXT,
    first_bed_medical_status TEXT,
    second_bed_medical_status TEXT,
    post_acute_medical_status TEXT,
    second_bed_specialty_resource_1 TEXT,
    second_bed_specialty_resource_2 TEXT,
    second_bed_specialty_resource_3 TEXT,
    post_acute_resource_1 TEXT,
    post_acute_resource_2 TEXT,
    post_acute_resource_3 TEXT,
    post_acute_resource_4 TEXT,
    post_acute_resource_5 TEXT
);
