from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from datetime import datetime

# document_only to mark child collections to be excluded from schema, but not autodoc
# exclude=True to include in redcap, but exclude from documentation
# hidden=True to include in redcap and documentation, but mark as HIDDEN field i redcap
# transfer_only =True to include in dump_data, but exclude from redcap and documentation

# ============================================================
# Felles kode-/verdi-struktur
# ============================================================

class Code(BaseModel):
    v: Optional[str] = Field(None, title="Kode")
    dn: Optional[str] = Field(None, title="Vist verdi")
    term: Optional[str] = Field(None, title="Terminologi")

class CodeValue(BaseModel):
    magnitude: Optional[float] = Field(None, title="Målt verdi")
    unit: Optional[str] = Field(None, title="Enhet")

class CodeValueBoth(BaseModel):
    v: Optional[str] = Field(None, title="Kode")
    dn: Optional[str] = Field(None, title="Vist verdi")
    term: Optional[str] = Field(None, title="Terminologi")
    magnitude: Optional[float] = Field(None, title="Målt verdi")
    unit: Optional[str] = Field(None, title="Enhet")

# ============================================================
# Admin
# ============================================================

class Admin(BaseModel):
    redcap_repeat_instance: str = Field('new',  json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('admin',  json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG") # MÅ være med én gang

    sent_organisation: Optional[str] = Field(None, title="Tilhørende HF")
    patient_id: Optional[str] = Field(
        None, 
        title="Pasient-ID", 
        description="F.eks. fødselsnummer eller D-nummer",
        json_schema_extra={
            "document_only": True # Skal ikke i REDCap
        }
    )
    patient_id_type: Optional[str] = Field(
        None, 
        title="Pasient-ID-type", 
        description="Type identifikator som er brukt for pasienten, f.eks. 'Fødselsnummer' eller 'D-nummer'",
        json_schema_extra={
            "document_only": True
        }
    )

    patient_postalcode: Optional[str] = Field(None, title="Postnummer", json_schema_extra={"document_only": True})
    patient_county: Optional[str] = Field(None, title="Fylke", json_schema_extra={"document_only": True})

# ============================================================
# Course
# ============================================================

class Course(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('course', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    crs_id: Optional[str] = Field(None, title="Course ID", json_schema_extra={"hidden": True})
    sent_dt: Optional[datetime] = Field(None, title="Sendingstidspunkt eksportskjema")
    export_template_id: Optional[str] = Field(None, title="Innrapporteringsskjema versjon")

    crs_tumor_group: Optional[Code] = Field(
        None, 
        title="Forløpstype", 
        description="Hvilken type kreftsykdom forløpet gjelder"
    )

    crs_inform_norpreg: Optional[Code] = Field(
        None, 
        title="Informert pasienten om reservasjon til NORPREG",
        description="Om pasienten er informert om muligheten til å reservere seg mot registrering i NORPREG"
    )

    clinics: List["Clinic"] = Field(
        default_factory=List, 
        exclude=True, 
        title="Clinic-tabell",
        json_schema_extra={
            "document_only": True
        }
    )
    studies: List["Studies"] = Field(
        default_factory=List, 
        exclude=True, 
        title="Studies-tabell",
        json_schema_extra={
            "document_only": True
        }
    )

# ============================================================
# Clinic
# ============================================================

class Clinic(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('clinic', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    cln_id: Optional[str] = Field(None, title="Clinic ID", json_schema_extra={"hidden": True})
    cln_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    cln_weight: Optional[CodeValue] = Field(None, title="Kroppsvekt ved diagnose (kg)")
    cln_height: Optional[CodeValue] = Field(None, title="Høyde  (cm)")

    cln_education: Optional[Code] = Field(None, title="Høyeste fullførte utdanningsnivå")
    cln_marital: Optional[Code] = Field(None, title="Samlivsstatus")
    cln_work: Optional[Code] = Field(None, title="Arbeidsstatus")

    cln_care_u18: Optional[Code] = Field(None, title="Omsorgsansvar barn < 18 år")
    cln_care_o18: Optional[Code] = Field(None, title="Omsorgsansvar voksne")

    cln_smoking: Optional[Code] = Field(None, title="Røyking")
    cln_smoking_qty: Optional[CodeValue] = Field(None, title="Røyking (pakkeår)")
    cln_other_tobacco: Optional[Code] = Field(None, title="Røykfri tobakk")

    cln_alcohol: Optional[Code] = Field(None, title="Alkoholbruk")
    cln_alcohol_qty: Optional[CodeValue] = Field(None, title="Alkoholforbruk (mengde)")

    cln_subj_hearing_imp: Optional[Code] = Field(None, title="Subjektiv hørselsnedsettelse", description="Brukes da CTCAE krever audimetri")
    cln_ecog: Optional[Code] = Field(None, title="ECOG funksjonsstatus")
    cln_karnofsky: Optional[Code] = Field(None, title="Karnofsky performance status")

    cln_ctnm_t: Optional[Code] = Field(None, title="Primærtumor (cT)")
    cln_ctnm_n: Optional[Code] = Field(None, title="Regionale lymfeknuter (cN)")
    cln_ctnm_m: Optional[Code] = Field(None, title="Fjernmetastase (cM)")
    cln_ctnm_r: Optional[Code] = Field(None, title="Residiv (r)")
    cln_ctnm_stage: Optional[Code] = Field(None, title="Klinisk stadium")

    cln_ptnm_t: Optional[Code] = Field(None, title="Primærtumor (pT)")
    cln_ptnm_n: Optional[Code] = Field(None, title="Regionale lymfeknuter (pN)")
    cln_ptnm_m: Optional[Code] = Field(None, title="Fjernmetastase (pM)")
    cln_ptnm_r: Optional[Code] = Field(None, title="Residiv (r)")

    cln_diagnosis: Optional[Code] = Field(None, title="Primærdiagnose (ICD-10)")

    cln_other_method: Optional[Code] = Field(None, title="Annen klassifisering (metode)")
    cln_other_result: Optional[Code] = Field(None, title="Annen klassifisering (resultat)")

    cln_multifocal: Optional[Code] = Field(None, title="Multifokal tumor")
    cln_multifocal_basis: Optional[Code] = Field(None, title="Multifokal tumor (grunnlag)")

    cln_multi_prim: Optional[Code] = Field(None, title="Multiple primærtumorer")
    cln_multi_prim_basis: Optional[Code] = Field(None, title="Multiple primære (grunnlag)")

    # child collections
    comorbidities: List["Comorbidity"] = Field(default_factory=List, exclude=True, title="Comorbidity-tabell", json_schema_extra={"document_only": True})
    prev_cancers: List["PrevCancer"] = Field(default_factory=List, exclude=True, title="PrevCancer-tabell", json_schema_extra={"document_only": True})
    prev_treatments: List["PrevTreatment"] = Field(default_factory=List, exclude=True, title="PrevTreatment-tabell", json_schema_extra={"document_only": True})
    adverse_events: List["Adverse"] = Field(default_factory=List, exclude=True, title="Adverse-tabell", json_schema_extra={"document_only": True})
    radiology: List["Radiology"] = Field(default_factory=List, exclude=True, title="Radiology-tabell", json_schema_extra={"document_only": True})
    anatomy: List["Anatomy"] = Field(default_factory=List, exclude=True, title="Anatomy-tabell", json_schema_extra={"document_only": True})
    anatomy_freetext: List["AnatomyFreeText"] = Field(default_factory=List, exclude=True, title="AnatomyFreeText-tabell", json_schema_extra={"document_only": True})
    mets: List["Mets"] = Field(default_factory=List, exclude=True, title="Mets-tabell", json_schema_extra={"document_only": True})
    lymph_mets: List["LymphMets"] = Field(default_factory=List, exclude=True, title="LymphMets-tabell", json_schema_extra={"document_only": True})
    lab_samples: List["LabSample"] = Field(default_factory=List, exclude=True, title="LabSample-tabell", json_schema_extra={"document_only": True})
    lab_tests: List["LabTest"] = Field(default_factory=List, exclude=True, title="LabTest-tabell", json_schema_extra={"document_only": True})
    treatment_summaries: List["TreatmentSummary"] = Field(default_factory=List, exclude=True, title="TreatmentSummary-tabell", json_schema_extra={"document_only": True})


# ============================================================
# Studies
# ============================================================

class Studies(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('studies', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    study_id: Optional[str] = Field(None, title="Studies ID", json_schema_extra={"hidden": True})
    study_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    study_name: Optional[str] = Field(None, title="Studienavn")
    study_comment: Optional[str] = Field(None, title="Kommentar")
    study_person: Optional[str] = Field(None, title="Kontaktperson")


# ============================================================
# Comorbidity
# ============================================================

class Comorbidity(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('comorbidity', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    cmrb_id: Optional[str] = Field(None, title="Comorbidity ID", json_schema_extra={"hidden": True})
    cmrb_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    cmrb_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    cmrb: Optional[Code] = Field(
        None, 
        title="Komorbiditet", 
        description="Brukes for å registrere komorbiditet ved diagnose, f.eks. hjerte- og karsykdom, diabetes, KOLS, " \
                    "nevrologisk sykdom etc. Kan være både spesifikke sykdommer (ICD10) og mer generelle kategorier av " \
                    "sykdommer (ICD10-kapitler"
    )

# ============================================================
# Previous cancer / treatment
# ============================================================

class PrevCancer(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('prev_cancer', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    prvc_id: Optional[str] = Field(None, title="PrevCancer ID", json_schema_extra={"hidden": True})
    prvc_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    prvc_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})
    prvc_prev_crs_id: Optional[str] = Field(None, title="PrevCancer Course ID (FK) (henviser til tidligere Course om den finnes)", json_schema_extra={"hidden": True})
    

    prvc_diag: Optional[Code] = Field(None, title="Tidligere kreftdiagnose")
    prvc_confirm_dt: Optional[datetime] = Field(None, title="Dato (ca) for tidligere kreftdiagnose")


class PrevTreatment(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('prev_treatment', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    prvt_id: Optional[str] = Field(None, title="PrevTreatment ID", json_schema_extra={"hidden": True})
    prvt_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    prvt_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})
    prvt_start_dt: Optional[datetime] = Field(None, title="Behandlingsstart")
    prvt_stop_dt: Optional[datetime] = Field(None, title="Behandlingsslutt")
    prvt_proc: Optional[Code] = Field(None, title="Prosedyre")


# ============================================================
# Adverse events
# ============================================================

class Adverse(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('adverse', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    ae_id: Optional[str] = Field(None, title="Adverse ID", json_schema_extra={"hidden": True})
    ae_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    ae_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    ae_added_dt: Optional[datetime] = Field(None, title="Dato for bivirkningsregistrering")
    ae_is_baseline: Optional[Code] = Field(None, title="Registrering er for baseline?")
    ae_cat: Optional[Code] = Field(None, title="Kategori for bivirkning")
    ae_term: Optional[Code] = Field(None, title="MedDRA-term for bivirkning")
    ae_grade: Optional[Code] = Field(None, title="CTCAE-gradering for bivirkning")


# ============================================================
# Radiology
# ============================================================

class Radiology(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('radiology', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    rad_id: Optional[str] = Field(None, title="Radiology ID", json_schema_extra={"hidden": True})
    rad_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    rad_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    rad_dt: Optional[datetime] = Field(None, title="Dato for undersøkelse")
    rad_modality: Optional[Code] = Field(None, title="Modalitet")
    rad_conclusion: Optional[Code] = Field(None, title="Resymé")

# ============================================================
# Anatomy
# ============================================================

class Anatomy(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('anatomy', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    anat_id: Optional[str] = Field(None, title="Anatomy ID", json_schema_extra={"hidden": True})
    anat_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    anat_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    anat_site: Optional[Code] = Field(None, title="Kroppssted")
    anat_specific_site: Optional[Code] = Field(None, title="Spesifikt sted")
    anat_side: Optional[Code] = Field(None, title="Kroppsside")


class AnatomyFreeText(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('anatomy_freetext', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    anat_free_id: Optional[str] = Field(None, title="AnatomyFreeText ID", json_schema_extra={"hidden": True})
    anat_free_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    anat_free_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})
    anat_site_txt: Optional[str] = Field(None, title="Kroppsted (fritekst)")
    anat_side_txt: Optional[str] = Field(None, title="Kroppsside (fritekst)")

# ============================================================
# Metastases
# ============================================================

class Mets(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('mets', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    mets_id: Optional[str] = Field(None, title="Mets ID", json_schema_extra={"hidden": True})
    mets_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    mets_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    mets_line: Optional[Code] = Field(None, title="Anatomisk linje")
    mets_site: Optional[Code] = Field(None, title="Kroppssted")
    mets_side: Optional[Code] = Field(None, title="Kroppsside")
    mets_other_meth: Optional[str] = Field(None, title="Annen metode")

    methods: List["MetsMethod"] = Field(default_factory=List, exclude=True, title="MetsMethod-tabell", json_schema_extra={"document_only": True})


class LymphMets(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('lymph_mets', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    lmets_id: Optional[str] = Field(None, title="LymphMets ID", json_schema_extra={"hidden": True})
    lmets_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    lmets_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    lmets_line: Optional[Code] = Field(None, title="Anatomisk linje")
    lmets_site: Optional[Code] = Field(None, title="Kroppssted")
    lmets_side: Optional[Code] = Field(None, title="Kroppsside")
    lmets_other_meth: Optional[str] = Field(None, title="Annen metode")

    methods: List["MetsMethod"] = Field(default_factory=List, exclude=True, title="MetsMethod-tabell", json_schema_extra={"document_only": True})


class MetsMethod(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('mets_method', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    meth_id: Optional[str] = Field(None, title="MetsMethod ID", json_schema_extra={"hidden": True})
    meth_mets_id: Optional[str] = Field(None, title="Mets ID (FK)", json_schema_extra={"hidden": True})
    meth_lmets_id: Optional[str] = Field(None, title="LymphMets ID (FK)", json_schema_extra={"hidden": True})

    meth_meth: Optional[Code] = Field(
        None, 
        title="Grunnlag for diagnose", 
        description="Grunnlaget for diagnose av metastase, f.eks. klinisk, radiologisk, patologisk etc."
    )

# ============================================================
# Lab
# ============================================================

class LabSample(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('lab_sample', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    sample_id: Optional[str] = Field(None, title="Sample ID", json_schema_extra={"hidden": True})
    sample_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    sample_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    sample_req_id: Optional[str] = Field(None, title="Rekvisisjonsnummer")
    sample_name: Optional[str] = Field(None, title="Prøvemateriale navn/ID")
    sample_dt: Optional[datetime] = Field(None, title="Prøvedato")
    sample_method: Optional[Code] = Field(None, title="Prøvetakingsmetode")
    sample_type: Optional[Code] = Field(None, title="Type prøvemateriale")


class LabTest(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('lab_test', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    test_id: Optional[str] = Field(None, title="LabTest ID", json_schema_extra={"hidden": True})
    test_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    test_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})
    test_sample_id: Optional[str] = Field(None, title="Sample ID (FK)", json_schema_extra={"hidden": True})

    test_type: Optional[str] = Field(None, title="Type prøvetakingsmetode", description="F.eks. genetisk, virologisk, biologisk")
    test_name: Optional[Code] = Field(None, title="Analysenavn")
    test_result: Optional[CodeValueBoth] = Field(None, title="Resultat")

# ============================================================
# Treatment
# ============================================================

class TreatmentSurgery(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('tx_surgery', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    txsurg_id: Optional[str] = Field(None, title="TreatmentSurgery ID", json_schema_extra={"hidden": True})
    txsurg_txsum_id: Optional[str] = Field(None, title="TreatmentSummary ID (FK)", json_schema_extra={"hidden": True})
    txsurg_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    txsurg_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    txsurg_code: Optional[Code] = Field(None, title="Prosedyrekode")
    txsurg_target: Optional[Code] = Field(None, title="Operasjon utført for")
    txsurg_performed_dt: Optional[datetime] = Field(None, title="Dato for utført operasjon")


class TreatmentMedicine(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('tx_medicine', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    txmed_id: Optional[str] = Field(None, title="TreatmentMedicine ID", json_schema_extra={"hidden": True})
    txmed_txsum_id: Optional[str] = Field(None, title="TreatmentSummary ID (FK)", json_schema_extra={"hidden": True})
    txmed_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    txmed_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    txmed_rx_name: Optional[str] = Field(None, title="Navn på legemiddel / virkestoff / kur")
    txmed_category: Optional[Code] = Field(None, title="Behandlingskategori / type MKB")
    txmed_dose: Optional[CodeValue] = Field(None, title="Totalmengde i perioden")
    txmed_start_dt: Optional[datetime] = Field(None, title="Startdato for bruk")
    txmed_stop_dt: Optional[datetime] = Field(None, title="Sluttdato for bruk")


class TreatmentRT(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('tx_radiotherapy', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    txrt_id: Optional[str] = Field(None, title="TreatmentRT ID", json_schema_extra={"hidden": True})
    txrt_txsum_id: Optional[str] = Field(None, title="TreatmentSummary ID (FK)", json_schema_extra={"hidden": True})
    txrt_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    txrt_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    txrt_type: Optional[Code] = Field(None, title="Type stråleterapi")
    txrt_first_fx_dt: Optional[datetime] = Field(None, title="Dato for første fraksjon")
    txrt_last_fx_dt: Optional[datetime] = Field(None, title="Dato for siste fraksjon")
    txrt_summary_txt: Optional[str] = Field(None, title="Oppsummering av dose og fraksjonering")
    txrt_reirr: Optional[Code] = Field(None, title="Kategori av rebestråling")
    txrt_comp: Optional[Code] = Field(None, title="Er det gjort en komparativ doseplan?")


class TreatmentSummary(BaseModel):
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('tx_summary', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    txsum_id: Optional[str] = Field(None, title="TreatmentSummary ID", json_schema_extra={"hidden": True})
    txsum_cln_id: Optional[str] = Field(None, title="Clinic ID (FK)", json_schema_extra={"hidden": True})
    txsum_crs_id: Optional[str] = Field(None, title="Course ID (FK)", json_schema_extra={"hidden": True})

    txsum_intention: Optional[Code] = Field(None, title="Behandlingsintensjon ved MDT")
    txsum_category: Optional[Code] = Field(None, title="Behandlingkategori (relativt til kirurgi)")
    txsum_description_txt: Optional[str] = Field(None, title="Ytterligere beskrivelse")
    txsum_surg_summary_txt: Optional[str] = Field(None, title="Overordnet beskrivelse av kirurgi")
    txsum_med_summary_txt: Optional[str] = Field(None, title="Overordnet beskrivelse av medikamentell behandling")
    txsum_rt_summary_txt: Optional[str] = Field(None, title="Overordnet beskrivelse av strålebehandling")

    surgeries: List["TreatmentSurgery"] = Field(default_factory=List, exclude=True, title="TreatmentSurgery-tabell", json_schema_extra={"document_only": True})
    medicines: List["TreatmentMedicine"] = Field(default_factory=List, exclude=True, title="TreatmentMedicine-tabell", json_schema_extra={"document_only": True})
    radiotherapy: List["TreatmentRT"] = Field(default_factory=List, exclude=True, title="TreatmentRT-tabell", json_schema_extra={"document_only": True})