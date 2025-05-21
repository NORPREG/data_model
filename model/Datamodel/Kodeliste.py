from typing_extensions import Annotated

from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field
from typing import Optional, List, Literal
from datetime import datetime

from .utils import field_with_meta

registries = {
    "NORPREG": "Norsk proton- og stråleterapiregister",
    "KREST-UNN": "Kvalitetsregister for stråleterapi Universitetssykehuset Nord-Norge", 
    "KREST-NLSH": "Kvalitetsregister for stråleterapi Nordlandssykehuset",
    "KREST-SOH": "Kvalitetsregister for stråleterapi St. Olavs hospital",
    "KREST-AAL": "Kvalitetsregister for stråleterapi Ålesund sjukehus",
    "KREST-HUS": "Kvalitetsregister for stråleterapi Haukeland universitetssykehus",
    "KREST-SUS": "Kvalitetsregister for stråleterapi Stavanger universitetssykehus",
    "KREST-SSHF": "Kvalitetsregister for stråleterapi Sørlandet sykehus",
    "KREST-SIG": "Kvalitetsregister for stråleterapi Sykehuset innlandet",
    "KREST-OUS": "Kvalitetsregister for stråleterapi Oslo universitetssykehus (formalisert 2025-01)"
}

class Registry(BaseModel):
    id: int
    name: Literal[tuple(registries.keys())] = field_with_meta(title="Registernavn", 
        description="Navn på registeret. Ikke alle registerne er formaliserte, så navnene kan unnvike. Formaliserte registre er markert.", 
        values=[f"{k}: {v}" for k,v in registries.items()])
    patients: List['Patient'] = field_with_meta(title="Tilknyttede pasienter", default_factory=list)
    registry_exports: List['RegistryExport'] = field_with_meta("Tilknyttede eksporter", default_factory=list)


class Patient(BaseModel):
    """Pasientobjekt. Kan inneholde flere behandlingsforløp."""
    
    patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret. Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)")
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når pasienten ble lagt inn i registeret. Angis når enten DICOM-datasettet eller EPJ-datasettet ankommer.")

    fk_registry_id: int = field_with_meta(title="FK registernøkkel", description="")
    registry: Optional[Registry] = field_with_meta(title="Tilhørende register", description="Hvilket KREST ligger pasienten i? Dersom det er flere, som i behandling ved lokalsykehus, gjelder første.", default=None)

    patient_ids: List['PatientID'] = field_with_meta(title="Pasient ID-er", description="Liste over pasientens tilhørende F / D / H - nummer", default_factory=list)
    addresses: List['Address'] = field_with_meta(title="Adresser", description="Pasientens tilhørende adresser", default_factory=list)
    courses: List['Course'] = field_with_meta(title="Behandlingsforløp", description="Pasientens tilhørende behandlingsforløp. Knyttet til Course ID i OIS og sak i DIPS.", default_factory=list)
    patient_exports: List['PatientExport'] = field_with_meta(title="Datautleveringer", description="Datautleveringer knyttet til pasienten", default_factory=list)
    pvk_events: List['PvkEvent'] = field_with_meta(title="Personvernkomponent-hendelser", description="Pasientens reservasjoner og trukkede reservasjoner", default_factory=list)

    name_aes: str = field_with_meta(title="Pasientens navn som angitt i DICOM", 
        description="Må se hvordan fornavn og etternavn deles opp når det kommer fra PAS i DIPS, så skjer nok en liten endring her. I DICOM benyttes ETTERNAVN^FORNAVN.", encrypted=True)
    birth_date_aes: str = field_with_meta(title="Pasientens fødselsdato", description="", encrypted=True, unit="YYYY-MM-DD")
    ois_patient_id_aes: str = field_with_meta(title="OIS pasient ID", description="PasientID i stråleterapisystem (f.eks. PatientSer i Aria)", encrypted=True)
    epj_patient_id_aes: str = field_with_meta(title="EPJ pasient ID", description="PasientID i journalsystem", encrypted=True)


class PatientID(BaseModel):
    """En av flere av F/D/H-numrene til pasienten. 
    
        Oppdateres med nytt nummer når dette blir tilgjengelig. 
        PVK håndterer bl.a. dette smidig hvor nyeste fnr alltid returneres.
        Behøver rutine for å fange når det skjer oppdateringer."""

    id: int = field_with_meta(title="Radindeks for pasient ID", description="Pseudonymisert nøkkel for pasienten i registeret.")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="", description="", default=None)
    dt_added: datetime = field_with_meta(title="", description="")
    fnr_aes: str = field_with_meta(title="", description="", encrypted=True)
    fnr_type: str = field_with_meta(title="", description="")


class Address(BaseModel):
    """Benytt ``dt_added`` for å tolke postnummer, kommunenummer etter da gjeldende standard."""

    id: int = field_with_meta(title="Radindeks for adresse", description="Dannes automatisk ved opprettelse av ny adresse")
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når aktuell adresse ble lagt til")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="")

    zip_code_aes: str = field_with_meta(title="Postnummer", description="Postnummer da pasienten ble lagt inn", encrypted=True)
    bydel_aes: str = field_with_meta(title="Bydel", description="Aktuell for Oslo.", encrypted=True)
    kommune_nr_aes: str = field_with_meta(title="Kommunenummer", description="Kommunenummer da pasienten ble lagt inn", encrypted=True)


class Course(BaseModel):
    """Tabell for behandlingsforløp"""

    id: int = field_with_meta(title="Radindeks for behandlingsforløp", description="Dannes automatisk ved opprettelse av nytt behandlingsforløp")
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når aktuelt behandlingsforløp ble lagt til")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="", description="", default=None)
    patient_exports: List['PatientExport'] = field_with_meta(title="", description="", default_factory=list)
    fk_datastatus_id: int = field_with_meta(title="", description="")
    data_status: Optional['DataStatus'] = field_with_meta(title="", description="", default=None)
    ois_course_id: str = field_with_meta(title="", description="")
    epj_course_id: str = field_with_meta(title="", description="")


class DataStatus(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    fk_course_id: int = field_with_meta(title="", description="")
    course: Optional[Course] = field_with_meta(title="", description="", default=None)
    epj_status_aes: int = field_with_meta(title="", description="", encrypted=True)
    dicom_status_aes: int = field_with_meta(title="", description="", encrypted=True)
    consent_status_aes: int = field_with_meta(title="", description="", encrypted=True)
    prom_status_aes: int = field_with_meta(title="", description="", encrypted=True)


class Study(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    conquest_name: str = field_with_meta(title="", description="")
    description_aes: str = field_with_meta(title="", description="", encrypted=True)
    contact_person_aes: str = field_with_meta(title="", description="", encrypted=True)
    institution_aes: str = field_with_meta(title="", description="", encrypted=True)
    email_aes: str = field_with_meta(title="", description="", encrypted=True)
    store_until: datetime = field_with_meta(title="", description="")

    exports: List['Export'] = field_with_meta(title="", description="", default_factory=list)


class Export(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    fk_study_id: int = field_with_meta(title="", description="")
    study: Optional[Study] = field_with_meta(title="", description="", default=None)
    patient_exports: List['PatientExport'] = field_with_meta(title="", description="", default_factory=list)
    registry_exports: List['RegistryExport'] = field_with_meta(title="", description="", default_factory=list)
    export_date: datetime = field_with_meta(title="", description="")
    contact_person_aes: str = field_with_meta(title="", description="", encrypted=True)
    institution_aes: str = field_with_meta(title="", description="", encrypted=True)
    email_aes: str = field_with_meta(title="", description="", encrypted=True)
    mechanism: str = field_with_meta(title="", description="")
    is_pseudo: bool = field_with_meta(title="", description="")


class PatientExport(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="", description="", default=None)
    fk_course_id: int = field_with_meta(title="", description="")
    course: Optional[Course] = field_with_meta(title="", description="", default=None)
    fk_export_id: int = field_with_meta(title="", description="")
    export: Optional[Export] = field_with_meta(title="", description="", default=None)
    pseudo_key_aes: str = field_with_meta(title="", description="", encrypted=True)


class RegistryExport(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    fk_registry_id: int = field_with_meta(title="", description="")
    registry: Optional[Registry] = field_with_meta(title="", description="", default=None)
    fk_export_id: int = field_with_meta(title="", description="")
    export: Optional[Export] = field_with_meta(title="", description="", default=None)


class PvkEvent(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    event_time: datetime = field_with_meta(title="", description="")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="", description="", default=None)
    fk_sync_id: int = field_with_meta(title="", description="")
    pvk_sync: Optional['PvkSync'] = field_with_meta(title="", description="", default=None)
    is_reserved_aes: bool = field_with_meta(title="", description="", encrypted=True)


class PvkSync(BaseModel):
    id: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret.")
    pvk_events: List[PvkEvent] = field_with_meta(title="", description="", default_factory=list)
    dt_sync: datetime = field_with_meta(title="", description="")
    new_reservations: int = field_with_meta(title="", description="")
    new_reservation_removals: int = field_with_meta(title="", description="")
    error_message: str = field_with_meta(title="", description="")