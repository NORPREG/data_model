from unittest.util import strclass
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import date, datetime

from .utils import field_with_meta

education_levels = {
	0: "Ingen utdanning",
	1: "Grunnskole",
	2: "Videregående",
	3: "Universitet / høyskole < 4 år",
	4: "Universitet / høyskole >= 4 år",
	9: "Ukjent"
}

ecog_levels = {
	0: "Asymptomatisk i stand til å utføre enhver normal aktivitet uten begrensning",
	1: "Symptomatisk, fullt oppegående Ikke i stand til fysisk krevende aktivitet, men oppegående og i stand til å utføre lett arbeid",
	2: "Symptomatisk, sengeliggende <50 % av våken tid Oppegående og i stand til all egenpleie, men ikke i stand til noe arbeid; oppe og i bevegelse mer enn 50% av våken tid",
	3: "Symptomatisk, sengeliggende > 50 % av våken tid Bare i stand til begrenset egenpleie, bundet til seng eller stol > 50 % av våken tid",
	4: "Helt sengeliggende Helt hjelpetrengende; klarer ikke noen egenpleie; helt bundet til seng eller stol",
	5: "Pasienten er død"
}

marital_levels = {
	1: "Ugift",
	2: "Gift / Registrert partner",
	3: "Enke / enkemann / gjenlevende partner",
	4: "Skilt / Separert",
	9: "Ukjent"
}

arbeid_levels = {
	1: "I arbeid",
	2: "Ikke i arbeid",
	3: "Alderspensjonist",
	4: "Under utdanning / studerer",
	9: "Ukjent"
}

def parse(d: dict) -> list:
	return [f"{k}: {v}" for k,v in d.items()]

class Metadata(BaseModel):
	xml_timestamp: datetime
	xml_version_major: int = 0
	xml_version_minor: int = 3

class Demographics(BaseModel):
	rt_center: str = field_with_meta(title="", description="")
	referring_hf: str = field_with_meta(title="", description="")
	birth_year: int = field_with_meta(title="", description="")
	sex: Literal["mann", "kvinne"] = field_with_meta(title="", description="", values=["Mann", "Kvinne"])

class Vitals(BaseModel):
	weight_at_diagnosis_kg: float = field_with_meta(title="", description="")
	height_cm: float = field_with_meta(title="", description="")

class Social(BaseModel):
	education_level: Literal[tuple(education_levels.keys())] = \
		field_with_meta(title="Høyeste fullførte utdanningsnivå",
		terminology="no.utdanningsnivaa",
		values=parse(education_levels))

	martial_status: Literal[tuple(marital_levels.keys())]  = field_with_meta(title="Samlivsstatus", description="Det finnes lokale, myndighetspålagte verdisett eller terminologier som for eksempel SNOMED CT eller lignende", 
		values=parse(marital_levels), terminology="no.samlivsstatus")

	living_arrangements: Literal[
		"Ikke i parforhold",
		"Samboer/lever i parforhold",
		"Parforhold, lever ikke sammen / særbo",
		"Ukjent"
	]  = field_with_meta(title="", description="")

	arbeidsstatus: Literal[tuple(arbeid_levels.keys())] = \
		field_with_meta(title="Arbeidsstatus", values=parse(arbeid_levels), terminology="no.arbeidsstatus")

class Stimulantia(BaseModel):
	smoking_status: Literal[
		"Aldri røykt",
		"Røyker",
		"Tidligere røyker"
	]  = field_with_meta(title="", description="")

	pack_years: int  = field_with_meta(title="", description="")
	month_since_stopping: Optional[int] = field_with_meta(title="", description="", default=None)
	non_smoking_tobacco_status: Literal[
		"Aldri brukt",
		"Nåværende bruker",
		"Tidligere bruker"
	]  = field_with_meta(title="", description="")
	
	# Evaluation.Alkoholanamnese_v1 @ CKM
	alcohol_abuse: Literal[
		"Nåværende bruker",
		"TIdligere bruker",
		"Aldri brukt" 
	]  = field_with_meta(title="", description="")

class FunctionStatus(BaseModel):
	ecog_grade: Literal[tuple(ecog_levels.keys())]  = field_with_meta(title="ECOG", 
		description="Funksjonsstatus", values = [f"{k}: {v}" for k,v in ecog_levels.items()])
	ecog_date: date = field_with_meta(title="Dato for ECOG", description="Dato for pasientbesøk hvor ECOG ble vurdert", unit="YYYY-MM-DD")

class Comorbidity(BaseModel):
	comorbidity_name: Optional[str] = None
	comorbidity_code: Optional[str] = None
	comorbidity_term: Optional[str] = None
	comorbidity_terminology_version: Optional[str] = None

	comorbidity_category: Optional[str] = None
#	comorbidity_comment: Optional[str] = None
	comorbidity_date: date

class PrimaryDiagnosis(BaseModel):
	diagnosis_name: str
	diagnosis_code: str
	diagnosis_term: str
	diagnosis_edition: str
	multiple_primaries: bool
	
#	diagnosis_laterality: Optional[str] = None
	diagnosis_localisation: Optional[str] = None
	diagnosis_date: date
	diagnosis_method: str
#	diagnosis_comment: Optional[str] = None

class Staging(BaseModel):
	tnm_t: str
	tnm_n: str
	tnm_m: str

	tnm_string: str
	tnm_edition: str
	tnm_stage: Optional[str] = None
	
	# Brukes U, yC, yP i Norge?
	tnm_type: Literal["C", "P", "U", "yC", "yP"]
	other_type: Optional[str] = None
	other_grade: Optional[str] = None
	is_relapse: bool
	staging_date: date

class Metastasis(BaseModel):
	metastasis_diagnosed: bool
	metastasis_localisation: Optional[str]

class Histology(BaseModel):
	histological_celltype_code: str
	histological_celltype_description: str
	topographical_mapping_code: str
	topographical_mapping_description: str

class Genetics(BaseModel):
	amino_acid_changes: str

class PreviousCancerItem(BaseModel):
	previous_cancer_icd10_code: str
	previous_cancer_icd10_description: str
	previous_cancer_laterality: Optional[str] = None
	previous_cancer_localisation: Optional[str] = None
	previous_cancer_diagnosis_year: int
	previous_cancer_rt_given: bool
#	previous_cancer_comment: Optional[str] = None

class PreviousCancer(BaseModel):
	is_previous_cancer: bool
	previous_cancer: List[PreviousCancerItem]

class TreatmentRadiotherapy(BaseModel):
	course_id: str
	procedure_nkpk_code: str
	procedure_nkpk_description: str
#	comment: Optional[str] = None

class TreatmentSurgery(BaseModel):
	procedure_nkpk_code: str
	procedure_nkpk_description: str
	surgery_target: Literal[
		"Primærtumor",
		"Lokalt residiv og primærtumor",
		"Metastase"
	]
	surgery_date: date
#	comment: Optional[str] = None

class TreatmentSystemic(BaseModel):
	"""Legemiddel versus MKB?"""

	systemic_name: str # navn på legemiddel / virkestoff / kur
	category: Literal[
		"Kjemoterapi",
		"Immunterapi",
		"Hormonell behandling",
		"Målrettet terapi / small molecules"
	]

	therapeutic_intent: Literal[
		"Preoperativt",
		"Postoperativt"
	]

	total_dosage_value: float
	total_dosage_unit: str
	dosage_start_date: date
	dosage_stop_date: date
#	comment: Optional[str] = None

class TreatmentSummary(BaseModel):
	treatment_intention: Literal[
		"Kurativt",
		"Ikke kurativt (livsforlengende)",
		"Ikke kurativt (symptomlindrende)",
		"Ikke kurativt (lokalkontroll)"
	]
	treatment_type: Literal[
		"Neoadjuvant", 
		"Konkomitant", 
		"Adjuvant", 
		"Neoadjuvant + konkomitant", 
		"Neoadjuvant + adjuvant", 
		"Konkomitant + adjuvant", 
		"Neoadjuvant + konkomitant + adjuvant"
	]

	treatment_radiotherapy: Optional[TreatmentRadiotherapy] = None
	treatment_systemic: Optional[TreatmentSystemic] = None
	treatment_surgery: Optional[TreatmentSurgery] = None

class BiologicalSample(BaseModel):
	requisition_remissenr: str
	sample_laboratory: Optional[str] = None
	conclusion: str
	sample_date: date
	sample_type: Optional[Literal["Celler (cytologi)", "Vev", "Annet materiale"]] = None
	sample_anatomical_location: Optional[str] = None
	sample_tumorcells_percentage: Optional[float] = None
#	sample_comment: Optional[str] = None

class Biomarker(BaseModel):
	biomarker_name: str
	# biomarker_type: Literal["Diagnose", "Prognose", "Prediksjon"]
	biomarker_value: Optional[float] = None
	biomarker_unit: Optional[str] = None
	biomarker_result: Optional[Literal["Positiv", "Negativ", "Ikke undersøkt"]] = None
	biomarker_method: Optional[str] = None
#	comment: Optional[str] = None

class CTCAE(BaseModel):
	ctcae_date: date
	meddra_category: Optional[str] = None
	meddra_name: Optional[str] = None
	ctcae_grade: Literal[0,1,2,3,4,5]
	ctcae_terminology_version: Optional[str] = None
	meddra_terminology_version: Optional[str] = None
#	comment: Optional[str] = None

class VitalStatus(BaseModel):
	last_followup: Optional[date] = None # siste polikliniske kontakt
	mors_date: Optional[date] = None

class TumorEvent(BaseModel):
	progression_date: date
	progression_type: Literal["Progresjon", "Residiv"]
	progression_identification: Optional[
		Literal[
			"Histologi",
			"Radiologi",
			"Klinikk",
			"Biokjemisk",
			"Ukjent"
		]
	]
	progression_grade: Literal[
		"Lokal progresjon",
		"Regional progresjon",
		"Fjernmetastase"
	]
#	comment: Optional[str] = None
	
class Consent(BaseModel):
	informed_patient_about_rt_registry: bool
	informed_patient_about_broad_consent: bool

class ClinicalStudy(BaseModel):
	study_name: str
	study_contact_person: Optional[str] = None
#	comment: Optional[str] = None