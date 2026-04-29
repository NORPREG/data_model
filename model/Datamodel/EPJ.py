from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from datetime import datetime

from .utils import field_with_meta

# document_only to mark child collections to be excluded from schema, but not autodoc
# exclude=True to include in redcap, but exclude from documentation
# hidden=True to include in redcap and documentation, but mark as HIDDEN field i redcap
# transfer_only =True to include in dump_data, but exclude from redcap and documentation

# ============================================================
# Felles kode-/verdi-struktur
# ============================================================

class Code(BaseModel):
    """Basemodell for kodeverdi-par, som brukes mange steder i datamodellen. Inneholder både kodeverdi, vist verdi og terminologi."""
    v: Optional[str] = field_with_meta(title="Kode")
    dn: Optional[str] = field_with_meta(title="Vist verdi")
    term: Optional[str] = field_with_meta(title="Terminologi")

class CodeValue(BaseModel):
    """Basemodell for kodeverdi-par med tilhørende målt verdi og enhet, som brukes mange steder i datamodellen."""
    magnitude: Optional[float] = field_with_meta(title="Målt verdi")
    unit: Optional[str] = field_with_meta(title="Enhet")

class CodeValueBoth(BaseModel):
    """Basemodell for kodeverdi-par med tilhørende målt verdi og enhet, samt kodeverdi/vist verdi og terminologi. Brukes enkelte steder i datamodellen."""
    v: Optional[str] = field_with_meta(title="Kode")
    dn: Optional[str] = field_with_meta(title="Vist verdi")
    term: Optional[str] = field_with_meta(title="Terminologi")
    magnitude: Optional[float] = field_with_meta(title="Målt verdi")
    unit: Optional[str] = field_with_meta(title="Enhet")

# ============================================================
# Admin
# ============================================================

class Admin(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG") # MÅ være med én gang

    sent_organisation: Optional[str] = field_with_meta(title="Tilhørende HF")
    patient_id: Optional[str] = Field(
        None, 
        alias="Pasient-ID", 
        description="F.eks. fødselsnummer eller D-nummer",
        document_only=True
    )
    patient_id_type: Optional[str] = Field(
        None, 
        alias="Pasient-ID-type", 
        description="Type identifikator som er brukt for pasienten, f.eks. 'Fødselsnummer' eller 'D-nummer'",
        document_only=True

    )

    patient_postalcode: Optional[str] = field_with_meta(title="Postnummer", document_only=True)
    patient_county: Optional[str] = field_with_meta(title="Fylke", document_only=True)

# ============================================================
# Course
# ============================================================

class Course(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    crs_id: Optional[str] = field_with_meta(title="Course ID", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)
    sent_dt: Optional[datetime] = field_with_meta(title="Sendingstidspunkt eksportskjema")
    export_template_id: Optional[str] = field_with_meta(title="Innrapporteringsskjema versjon")

    crs_tumor_group: Optional[Code] = field_with_meta(
        title="Forløpstype", 
        description="Hvilken overordnet kreftsykdom forløpet gjelder"
    )

    crs_inform_norpreg: Optional[Code] = field_with_meta(
        title="Informert pasienten om reservasjon til NORPREG",
        description="Om pasienten er informert om muligheten til å reservere seg mot registrering i NORPREG."
    )

    clinics: List["Clinic"] = Field(
        default_factory=list, 
        exclude=True, 
        alias="Clinic-tabell",
        document_only=True,
        hidden=True
    )
    studies: List["Studies"] = Field(
        default_factory=list, 
        exclude=True, 
        alias="Studies-tabell",
        document_only=True,
        hidden=True
    )

# ============================================================
# Clinic
# ============================================================

class Clinic(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    cln_id: Optional[str] = field_with_meta(title="Clinic ID", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    cln_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    cln_weight: Optional[CodeValue] = field_with_meta(title="Kroppsvekt ved diagnose", unit="kg")
    cln_height: Optional[CodeValue] = field_with_meta(title="Høyde", unit="cm")

    cln_education: Optional[Code] = field_with_meta(title="Høyeste fullførte utdanningsnivå")
    cln_marital: Optional[Code] = field_with_meta(title="Samlivsstatus")
    cln_work: Optional[Code] = field_with_meta(title="Arbeidsstatus")

    cln_care_u18: Optional[Code] = field_with_meta(title="Omsorgsansvar barn < 18 år")
    cln_care_o18: Optional[Code] = field_with_meta(title="Omsorgsansvar voksne")

    cln_smoking: Optional[Code] = field_with_meta(title="Røyking")
    cln_smoking_qty: Optional[CodeValue] = field_with_meta(title="Røyking", unit="pakkeår")
    cln_other_tobacco: Optional[Code] = field_with_meta(title="Røykfri tobakk")

    cln_alcohol: Optional[Code] = field_with_meta(title="Alkoholbruk")
    cln_alcohol_qty: Optional[CodeValue] = field_with_meta(title="Alkoholforbruk (mengde)")

    cln_subj_hearing_imp: Optional[Code] = field_with_meta(title="Subjektiv hørselsnedsettelse", description="Brukes da CTCAE krever audimetri")
    cln_ecog: Optional[Code] = field_with_meta(title="ECOG funksjonsstatus")
    cln_karnofsky: Optional[Code] = field_with_meta(title="Karnofsky performance status")

    cln_ctnm_t: Optional[Code] = field_with_meta(title="Primærtumor (cT)")
    cln_ctnm_n: Optional[Code] = field_with_meta(title="Regionale lymfeknuter (cN)")
    cln_ctnm_m: Optional[Code] = field_with_meta(title="Fjernmetastase (cM)")
    cln_ctnm_r: Optional[Code] = field_with_meta(title="Residiv (r)")
    cln_ctnm_stage: Optional[Code] = field_with_meta(title="Klinisk stadium")

    cln_ptnm_t: Optional[Code] = field_with_meta(title="Primærtumor (pT)")
    cln_ptnm_n: Optional[Code] = field_with_meta(title="Regionale lymfeknuter (pN)")
    cln_ptnm_m: Optional[Code] = field_with_meta(title="Fjernmetastase (pM)")
    cln_ptnm_r: Optional[Code] = field_with_meta(title="Residiv (r)")

    cln_diagnosis: Optional[Code] = field_with_meta(title="Primærdiagnose", terminology="ICD10")

    cln_other_method: Optional[Code] = field_with_meta(title="Annen klassifisering (metode)")
    cln_other_result: Optional[Code] = field_with_meta(title="Annen klassifisering (resultat)")

    cln_multifocal: Optional[Code] = field_with_meta(title="Multifokal tumor")
    cln_multifocal_basis: Optional[Code] = field_with_meta(title="Multifokal tumor (grunnlag)")

    cln_multi_prim: Optional[Code] = field_with_meta(title="Multiple primærtumorer")
    cln_multi_prim_basis: Optional[Code] = field_with_meta(title="Multiple primære (grunnlag)")

    # child collections
    """
    comorbidities: List["Comorbidity"] = Field(default_factory=list, exclude=True, alias="Comorbidity-tabell", document_only=True)
    prev_cancers: List["PrevCancer"] = Field(default_factory=list, exclude=True, alias="PrevCancer-tabell", document_only=True)
    prev_treatments: List["PrevTreatment"] = Field(default_factory=list, exclude=True, alias="PrevTreatment-tabell", document_only=True)
    adverse_events: List["Adverse"] = Field(default_factory=list, exclude=True, alias="Adverse-tabell", document_only=True)
    radiology: List["Radiology"] = Field(default_factory=list, exclude=True, alias="Radiology-tabell", document_only=True)
    anatomy: List["Anatomy"] = Field(default_factory=list, exclude=True, alias="Anatomy-tabell", document_only=True)
    anatomy_freetext: List["AnatomyFreeText"] = Field(default_factory=list, exclude=True, alias="AnatomyFreeText-tabell", document_only=True)
    mets: List["Mets"] = Field(default_factory=list, exclude=True, alias="Mets-tabell", document_only=True)
    lymph_mets: List["LymphMets"] = Field(default_factory=list, exclude=True, alias="LymphMets-tabell", document_only=True)
    lab_samples: List["LabSample"] = Field(default_factory=list, exclude=True, alias="LabSample-tabell", document_only=True)
    lab_tests: List["LabTest"] = Field(default_factory=list, exclude=True, alias="LabTest-tabell", document_only=True)
    treatment_summaries: List["TreatmentSummary"] = Field(default_factory=list, exclude=True, alias="TreatmentSummary-tabell", document_only=True)
    """

# ============================================================
# Studies
# ============================================================

class Studies(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    study_id: Optional[str] = field_with_meta(title="Studies ID", hidden=True)
    study_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    study_name: Optional[str] = field_with_meta(title="Studienavn")
    study_comment: Optional[str] = field_with_meta(title="Kommentar")
    study_person: Optional[str] = field_with_meta(title="Kontaktperson")


# ============================================================
# Comorbidity
# ============================================================

class Comorbidity(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    cmrb_id: Optional[str] = field_with_meta(title="Comorbidity ID", hidden=True)
    cmrb_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    cmrb_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    cmrb: Optional[Code] = field_with_meta(
        title="Komorbiditet", 
        description="Brukes for å registrere komorbiditet ved diagnose, f.eks. hjerte- og karsykdom, diabetes, KOLS, " \
                    "nevrologisk sykdom etc. Kan være både spesifikke sykdommer (ICD10) og mer generelle kategorier av " \
                    "sykdommer (ICD10-kapitler)",
        terminology="ICD10"
    )

# ============================================================
# Previous cancer / treatment
# ============================================================

class PrevCancer(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    prvc_id: Optional[str] = field_with_meta(title="PrevCancer ID", hidden=True)
    prvc_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    prvc_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)
    prvc_prev_crs_id: Optional[str] = field_with_meta(title="PrevCancer Course ID (FK)", description="Henviser til *tidligere* Course ID om den finnes", hidden=True)

    prvc_diag: Optional[Code] = field_with_meta(title="Tidligere kreftdiagnose", terminology="ICD10")
    prvc_confirm_dt: Optional[datetime] = field_with_meta(title="Dato (ca) for tidligere kreftdiagnose")

class PrevTreatment(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    prvt_id: Optional[str] = field_with_meta(title="PrevTreatment ID", hidden=True)
    prvt_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    prvt_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)
    prvt_start_dt: Optional[datetime] = field_with_meta(title="Behandlingsstart")
    prvt_stop_dt: Optional[datetime] = field_with_meta(title="Behandlingsslutt")
    prvt_proc: Optional[Code] = field_with_meta(title="Prosedyre")


# ============================================================
# Adverse events
# ============================================================

class Adverse(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    ae_id: Optional[str] = field_with_meta(title="Adverse ID", hidden=True)
    ae_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    ae_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    ae_added_dt: Optional[datetime] = field_with_meta(title="Dato for bivirkningsregistrering")
    ae_is_baseline: Optional[Code] = field_with_meta(title="Registrering er for baseline?")
    ae_cat: Optional[Code] = field_with_meta(title="Kategori for bivirkning")
    ae_term: Optional[Code] = field_with_meta(title="Term for bivirkning", terminology="MedDRA")
    ae_grade: Optional[Code] = field_with_meta(title="Gradering for bivirkning", terminology="CTCAE")


# ============================================================
# Radiology
# ============================================================

class Radiology(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    rad_id: Optional[str] = field_with_meta(title="Radiology ID", hidden=True)
    rad_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    rad_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    rad_dt: Optional[datetime] = field_with_meta(title="Dato for undersøkelse")
    rad_modality: Optional[Code] = field_with_meta(title="Modalitet")
    rad_conclusion: Optional[Code] = field_with_meta(title="Resymé")

# ============================================================
# Anatomy
# ============================================================

class Anatomy(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    anat_id: Optional[str] = field_with_meta(title="Anatomy ID", hidden=True)
    anat_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    anat_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    anat_site: Optional[Code] = field_with_meta(title="Kroppssted")
    anat_specific_site: Optional[Code] = field_with_meta(title="Spesifikt sted")
    anat_side: Optional[Code] = field_with_meta(title="Kroppsside")


class AnatomyFreeText(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    anat_free_id: Optional[str] = field_with_meta(title="AnatomyFreeText ID", hidden=True)
    anat_free_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    anat_free_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)
    anat_site_txt: Optional[str] = field_with_meta(title="Kroppsted (fritekst)")
    anat_side_txt: Optional[str] = field_with_meta(title="Kroppsside (fritekst)")

# ============================================================
# Metastases
# ============================================================

class Mets(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    mets_id: Optional[str] = field_with_meta(title="Mets ID", hidden=True)
    mets_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    mets_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    mets_line: Optional[Code] = field_with_meta(title="Anatomisk linje")
    mets_site: Optional[Code] = field_with_meta(title="Kroppssted")
    mets_side: Optional[Code] = field_with_meta(title="Kroppsside")
    mets_other_meth: Optional[str] = field_with_meta(title="Annen metode")

    """
    methods: List["MetsMethod"] = Field(default_factory=list, exclude=True, alias="MetsMethod-tabell", document_only=True)
    """


class LymphMets(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    lmets_id: Optional[str] = field_with_meta(title="LymphMets ID", hidden=True)
    lmets_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    lmets_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    lmets_line: Optional[Code] = field_with_meta(title="Anatomisk linje")
    lmets_site: Optional[Code] = field_with_meta(title="Kroppssted")
    lmets_side: Optional[Code] = field_with_meta(title="Kroppsside")
    lmets_other_meth: Optional[str] = field_with_meta(title="Annen metode")

    """
    methods: List["MetsMethod"] = Field(default_factory=list, exclude=True, alias="MetsMethod-tabell", document_only=True)
    """


class MetsMethod(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    meth_id: Optional[str] = field_with_meta(title="MetsMethod ID", hidden=True)
    meth_mets_id: Optional[str] = field_with_meta(title="Mets ID (FK)", hidden=True)
    meth_lmets_id: Optional[str] = field_with_meta(title="LymphMets ID (FK)", hidden=True)

    meth_meth: Optional[Code] = field_with_meta(
        title="Grunnlag for diagnose", 
        description="Grunnlaget for diagnose av metastase, f.eks. klinisk, radiologisk, patologisk etc."
    )

# ============================================================
# Lab
# ============================================================

class LabSample(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    sample_id: Optional[str] = field_with_meta(title="Sample ID", hidden=True)
    sample_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    sample_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    sample_req_id: Optional[str] = field_with_meta(title="Rekvisisjonsnummer")
    sample_name: Optional[str] = field_with_meta(title="Prøvemateriale navn/ID")
    sample_dt: Optional[datetime] = field_with_meta(title="Prøvedato")
    sample_method: Optional[Code] = field_with_meta(title="Prøvetakingsmetode")
    sample_type: Optional[Code] = field_with_meta(title="Type prøvemateriale")


class LabTest(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    test_id: Optional[str] = field_with_meta(title="LabTest ID", hidden=True)
    test_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    test_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)
    test_sample_id: Optional[str] = field_with_meta(title="Sample ID (FK)", hidden=True)

    test_type: Optional[str] = field_with_meta(title="Type prøvetakingsmetode", description="F.eks. genetisk, virologisk, biologisk")
    test_name: Optional[Code] = field_with_meta(title="Analysenavn")
    test_result: Optional[CodeValueBoth] = field_with_meta(title="Resultat")

# ============================================================
# Treatment
# ============================================================

class TreatmentSurgery(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    txsurg_id: Optional[str] = field_with_meta(title="TreatmentSurgery ID", hidden=True)
    txsurg_txsum_id: Optional[str] = field_with_meta(title="TreatmentSummary ID (FK)", hidden=True)
    txsurg_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    txsurg_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    txsurg_code: Optional[Code] = field_with_meta(title="Prosedyrekode")
    txsurg_target: Optional[Code] = field_with_meta(title="Operasjon utført for")
    txsurg_performed_dt: Optional[datetime] = field_with_meta(title="Dato for utført operasjon")


class TreatmentMedicine(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    txmed_id: Optional[str] = field_with_meta(title="TreatmentMedicine ID", hidden=True)
    txmed_txsum_id: Optional[str] = field_with_meta(title="TreatmentSummary ID (FK)", hidden=True)
    txmed_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    txmed_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    txmed_rx_name: Optional[str] = field_with_meta(title="Navn på legemiddel / virkestoff / kur")
    txmed_category: Optional[Code] = field_with_meta(title="Behandlingskategori / type MKB")
    txmed_dose: Optional[CodeValue] = field_with_meta(title="Totalmengde i perioden")
    txmed_start_dt: Optional[datetime] = field_with_meta(title="Startdato for bruk")
    txmed_stop_dt: Optional[datetime] = field_with_meta(title="Sluttdato for bruk")


class TreatmentRT(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    txrt_id: Optional[str] = field_with_meta(title="TreatmentRT ID", hidden=True)
    txrt_txsum_id: Optional[str] = field_with_meta(title="TreatmentSummary ID (FK)", hidden=True)
    txrt_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    txrt_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    txrt_type: Optional[Code] = field_with_meta(title="Type stråleterapi")
    txrt_first_fx_dt: Optional[datetime] = field_with_meta(title="Dato for første fraksjon")
    txrt_last_fx_dt: Optional[datetime] = field_with_meta(title="Dato for siste fraksjon")
    txrt_summary_txt: Optional[str] = field_with_meta(title="Oppsummering av dose og fraksjonering")
    txrt_reirr: Optional[Code] = field_with_meta(title="Kategori av rebestråling")
    txrt_comp: Optional[Code] = field_with_meta(title="Er det gjort en komparativ doseplan?")


class TreatmentSummary(BaseModel):
    record_id: Optional[str] = field_with_meta(title="Pasientnøkkel i NORPREG", transfer_only=True)

    txsum_id: Optional[str] = field_with_meta(title="TreatmentSummary ID", hidden=True)
    txsum_cln_id: Optional[str] = field_with_meta(title="Clinic ID (FK)", description="Lages automatisk basert på innkommende eksportskjema fra EPJ", hidden=True)
    txsum_crs_id: Optional[str] = field_with_meta(title="Course ID (FK)", description="Koblingsnøkkel for behandlingsserie: hentes fra NPR-meldingen", hidden=True)

    txsum_intention: Optional[Code] = field_with_meta(title="Behandlingsintensjon ved MDT")
    txsum_category: Optional[Code] = field_with_meta(title="Behandlingkategori (relativt til kirurgi)")
    txsum_description_txt: Optional[str] = field_with_meta(title="Ytterligere beskrivelse")
    txsum_surg_summary_txt: Optional[str] = field_with_meta(title="Overordnet beskrivelse av kirurgi")
    txsum_med_summary_txt: Optional[str] = field_with_meta(title="Overordnet beskrivelse av medikamentell behandling")
    txsum_rt_summary_txt: Optional[str] = field_with_meta(title="Overordnet beskrivelse av strålebehandling")

    """
    surgeries: List["TreatmentSurgery"] = Field(default_factory=list, exclude=True, alias="TreatmentSurgery-tabell", document_only=True)
    medicines: List["TreatmentMedicine"] = Field(default_factory=list, exclude=True, alias="TreatmentMedicine-tabell", document_only=True)
    radiotherapy: List["TreatmentRT"] = Field(default_factory=list, exclude=True, alias="TreatmentRT-tabell", document_only=True)
    """