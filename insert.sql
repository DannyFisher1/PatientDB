INSERT INTO patient_cases (
    case_id, arrival_severity, gender, age, injury_icd10_1, injury_icd10_2, injury_ais_1, injury_ais_2, 
    combat_status, max_iss_score, mechanism_injury, primary_injury_type, secondary_injury_type, 
    tertiary_injury_type, medical_complications, first_bed_type, first_bed_hours, first_bed_start, 
    first_bed_end, second_bed_type, second_bed_hours, second_bed_start, second_bed_end, 
    post_acute_bed_type, post_acute_bed_hours, post_acute_bed_start, post_acute_bed_end, disposition, 
    primary_specialty, secondary_specialty, tertiary_specialty, other_specialty_resource_1, 
    other_specialty_resource_2, other_specialty_resource_3, first_bed_medical_status, 
    second_bed_medical_status, post_acute_medical_status, second_bed_specialty_resource_1, 
    second_bed_specialty_resource_2, second_bed_specialty_resource_3, post_acute_resource_1, 
    post_acute_resource_2, post_acute_resource_3, post_acute_resource_4, post_acute_resource_5
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
