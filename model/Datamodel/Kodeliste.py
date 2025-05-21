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
    """ De ulike registerne
        ===================
    """

    id: int = field_with_meta(title="Radindeks for registeret")
    name: Literal[tuple(registries.keys())] = field_with_meta(title="Registernavn", 
        description="Navn på registeret. Ikke alle registerne er formaliserte, så navnene kan unnvike. Formaliserte registre er markert.", 
        values=[f"{k}: {v}" for k,v in registries.items()])
    patients: List['Patient'] = field_with_meta(title="Tilknyttede pasienter", default_factory=list)
    registry_exports: List['RegistryExport'] = field_with_meta("Tilknyttede eksporter", default_factory=list)


class Patient(BaseModel):
    """Pasientobjekt
       =============
    
        Kan inneholde flere behandlingsforløp. Da benyttes samme pasient, som inneholder pekere mot flere `courses`."""

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
    """En av flere av F/D/H-numrene til pasienten
       ========================================== 
    
        Oppdateres med nytt nummer når dette blir tilgjengelig. 
        PVK håndterer bl.a. dette smidig hvor nyeste fnr alltid returneres.
        Behøver rutine for å fange når det skjer oppdateringer."""

    id: int = field_with_meta(title="Radindeks for pasient ID", description="Dannes automatisk ved opprettelse av hver pasient-ID")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    # patient: Optional[Patient] = field_with_meta(title="", description="", default=None)
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når denne pasient-ID-en ble lagt til i registeret")
    fnr_aes: str = field_with_meta(title="Pasientidentifikasjon", description="Kan være av ulik `fnr_type`", encrypted=True)
    fnr_type: Literal["F", "H", "D"] = field_with_meta(title="Type pasientidentifikasjon", 
        description="Dersom pasienten har flere tilknyttet seg, er det det siste F-nummeret som er gjeldende.", values=["F", "H", "D"])


class Address(BaseModel):
    """Tabell for adresser
       ===================
    
        Benytt ``dt_added`` for å tolke postnummer, kommunenummer etter da gjeldende standard."""

    id: int = field_with_meta(title="Radindeks for adresse", description="Dannes automatisk ved opprettelse av ny adresse")
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når aktuell adresse ble lagt til")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    # patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="")

    zip_code_aes: str = field_with_meta(title="Postnummer", description="Postnummer da pasienten ble lagt inn", encrypted=True)
    bydel_aes: str = field_with_meta(title="Bydel", description="Aktuell for Oslo.", encrypted=True)
    kommune_nr_aes: str = field_with_meta(title="Kommunenummer", description="Kommunenummer da pasienten ble lagt inn", encrypted=True)


class Course(BaseModel):
    """Tabell for behandlingsforløp
       ============================
    
    """

    id: int = field_with_meta(title="Radindeks for behandlingsforløp", description="Dannes automatisk ved opprettelse av nytt behandlingsforløp")
    dt_added: datetime = field_with_meta(title="Dato lagt til", description="Dato for når aktuelt behandlingsforløp ble lagt til")
    fk_patient_key: str = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="Pasientobjekt som hører til dette behandlingsforløpet", default=None)
    patient_exports: List['PatientExport'] = field_with_meta(title="", description="", default_factory=list)
    fk_datastatus_id: int = field_with_meta(title="FK datastatus ID", description="Koblingsnøkkel mot datastatus for dette behandlingsforløpet")
    data_status: Optional['DataStatus'] = field_with_meta(title="", description="", default=None)
    ois_course_id_aes: str = field_with_meta(title="OIS course ID", description="Koblingsnøkkel for behandlingsforløp / course i stråleterapisystem", encrypted=True)
    epj_course_id_aes: str = field_with_meta(title="EPJ course ID", description="Koblingsnøkkel for behandlingsforløp / sak i journalsystem", encrypted=True)


class DataStatus(BaseModel):
    id: int = field_with_meta(title="Radindeks for datastatus", description="Dannes automatisk ved opprettelse av ny statusmelding")
    fk_course_id: int = field_with_meta(title="FK course ID", description="Koblingsnøkkel for behandlingsforløp")
    course: Optional[Course] = field_with_meta(title="Tilknyttet behandlingsserie", description="Course-objekt som hører til denne datastatusen", default=None)
    fk_patient_key: str = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="Pasientobjekt som hører til denne datastatusen", default=None)
    epj_status_aes: int = field_with_meta(title="EPJ status", description="Statuskode for dataoverføring EPJ. Har behov for en god datamodell eller støttetabell her, f.eks. for å logge hver hendelse med statusmeldinger", encrypted=True)
    dicom_status_aes: int = field_with_meta(title="DICOM status", description="Statuskode for dataoverføring DICOM. Har behov for en god datamodell eller støttetabell her, f.eks. for å logge hver hendelse med statusmeldinger", encrypted=True)
    consent_status_aes: int = field_with_meta(title="PVK status", description="Statuskode for personvernkomponenten. Tabellene PvkSync og PvkEvents inneholder mer informasjon om mottate meldinger her", encrypted=True)
    prom_status_aes: int = field_with_meta(title="PROMs status", description="Statuskode for pasientrapporterte data. Har behov for en god datamodell eller støttetabell her, f.eks. for å logge hver hendelse med statusmeldinger", encrypted=True)


class Study(BaseModel):
    id: int = field_with_meta(title="Radindeks for studien", description="Dannes automatisk ved opprettelse av ny studie")
    conquest_name: str = field_with_meta(title="Conquest PACS AES title", description="Navnet på Conquest-instansen som er knyttet til dette studiet dersom det finnes")
    description_aes: str = field_with_meta(title="Studienavn", description="Navn på studien eller kvalitetsprosjektet", encrypted=True)
    contact_person_aes: str = field_with_meta(title="Kontaktperson", description="Registerets kontaktperson for denne studien", encrypted=True)
    institution_aes: str = field_with_meta(title="Institusjon", description="Hvor ledes studien fra", encrypted=True)
    email_aes: str = field_with_meta(title="Epost-adresse", description="Epost-adresse hvor kontaktpersonen kan nås", encrypted=True)
    store_until: datetime = field_with_meta(title="Datavarighet", description="Etter denne datoen slettes de ekstra dataene som er lagret for denne studien")

    exports: List['Export'] = field_with_meta(title="Datautleveringer", description="Hvilke datautleveringer som er knyttet mot denne studien", default_factory=list)


class Export(BaseModel):
    id: int = field_with_meta(title="Radindeks for utleveringen", description="Dannes automatisk ved opprettelse av ny utlevering")
    fk_study_id: int = field_with_meta(title="FK study ID", description="Koblingsnøkkel mot forskningsstudie / kvalitetsprosjekt for datautlevering")
    study: Optional[Study] = field_with_meta(title="", description="", default=None)
    patient_exports: List['PatientExport'] = field_with_meta(title="Pasientutleveringer", description="Mange-til-mange liste for pasienteksporter med enkeltvise unike pseudonymiserte nøkler", default_factory=list)
    registry_exports: List['RegistryExport'] = field_with_meta(title="Registerutleveringer", description="Mange-til-mange liste for koblinger mot enkeltvise registre i denne utleveringen", default_factory=list)
    export_date: datetime = field_with_meta(title="Utleveringsdato", description="Dato denne utleveringen fant sted (ikke søknadsdato)")
    contact_person_aes: str = field_with_meta(title="Kontaktperson", description="Kontaktperson for denne enkeltvise utleveringen", encrypted=True)
    institution_aes: str = field_with_meta(title="Institusjon", description="Institusjon for denne enkeltvise utleveringen", encrypted=True)
    email_aes: str = field_with_meta(title="Epost-adresse", description="Epost-adresse for kontaktpersonen", encrypted=True)
    mechanism: str = field_with_meta(title="Utleveringsmekanisme", description="Hvilken utleveringsmekanisme som er benyttet", values=["DICOM", "Filsluse", "USB", "Annet"])
    is_pseudo: bool = field_with_meta(title="Pseudonymiserte data", description="Er data pseudonymiserte?")


class PatientExport(BaseModel):
    """Pasient-eksport-koblingstabell
       ==============================
    
        Mange-til-mange koblingstabell for å håndtere pasientvise utleveringer"""

    id: int = field_with_meta(title="Radindeks for pasient-utleveringen", description="Dannes automatisk ved opprettelse av ny pasient-utlevering")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="Pasientobjekt som hører til denne eksporten", default=None)
    fk_course_id: int = field_with_meta(title="FK course ID", description="Koblingsnøkkel for behandlingsforløp")
    course: Optional[Course] = field_with_meta(title="Tilknyttet behandlingsserie", description="Course-objekt som hører til denne utleveringen", default=None)
    fk_export_id: int = field_with_meta(title="FK export ID", description="Koblingsnøkkel til utleveringstabell")
    export: Optional[Export] = field_with_meta(title="Tilknyttet utleveringsobjekt", description="Utleveringsobjekt som hører til denne utleveringen", default=None)
    pseudo_key_aes: str = field_with_meta(title="Pseudonymisert nøkkel", description="Pseudonymiseringsnøkkel knyttet til denne pasienten i denne utleveringen. Om ikke annet ønskes vil dette være en 5-hex tilfeldig streng (1 M muligheter)", encrypted=True)


class RegistryExport(BaseModel):
    """Register-eksport-koblingstabell
       ===============================
       
       Mange-til-mange koblingstabell for å hådntere registervise utleveringen"""

    id: int = field_with_meta(title="Radindeks for register-utlevering", description="PseudonymDannes automatisk ved opprettelse av ny register-utlevering.")
    fk_registry_id: int = field_with_meta(title="FK register ID", description="Koblingsnøkkel mot register ID")
    registry: Optional[Registry] = field_with_meta(title="Tilknyttet registerobjekt", description="Registerobjekt som hører til dene register-utleveringen", default=None)
    fk_export_id: int = field_with_meta(title="FK export ID", description="Koblingsnøkkel mot eksport ID")
    export: Optional[Export] = field_with_meta(title="Tilknyttet utleveringsobjekt", description="Utleveringsobjekt som hører til denne register-utleveringen", default=None)


class PvkEvent(BaseModel):
    """Pasientvis oppdatering fra Pvk
       ==============================
    
        Flere PvkEvents er koblet mot samme PvkSync. Den gjeldende statusen for en aktuell innbygger
        er gitt ved siste versjon (event_time) av alle PvkEvent som er knyttet mot innbyggeren."""

    id: int = field_with_meta(title="Radindeks for PvkEvent", description="Dannes automatisk ved opprettelse av ny PvkEvent")
    event_time: datetime = field_with_meta(title="Event time", description="Tidspunktet for avgitt svar på Helse Norge, benytt tidspunktet som angitt i API svar")
    fk_patient_key: int = field_with_meta(title="Registernøkkel", description="Pseudonymisert nøkkel for pasienten i registeret")
    patient: Optional[Patient] = field_with_meta(title="Tilknyttet pasient", description="Pasientobjekt som hører til denne PvkEventen", default=None)
    fk_sync_id: int = field_with_meta(title="FK PvkSync ID", description="Koblingsnøkkel mot en Pvk synkroniseringsinstans")
    pvk_sync: Optional['PvkSync'] = field_with_meta(title="Tilknyttet PvkSync-objekt", description="PvkSync-utleveringsobjekt som denne PvkEventen er knyttet mot", default=None)
    is_reserved_aes: str = field_with_meta(title="Reservasjon", description="Det faktiske svaret knyttet til denne PvkEventen. Sann dersom en gitt innbygger har reservert seg.", encrypted=True)


class PvkSync(BaseModel):
    """Tabell for enkeltvis Pvk-synkronisering
       ======================================="""

    id: int = field_with_meta(title="Radindeks for PvkSync", description="Dannes automatisk ved opprettelse av ny PvkSync")
    pvk_events: List[PvkEvent] = field_with_meta(title="PvkEvents", description="Tilknyttede PvkEvents for denne PvkSync-instansen", default_factory=list)
    dt_sync: datetime = field_with_meta(title="Sync datetime", description="Tidspunktet for PvkSync API-forespørsel. Benytter tidspunktet som angitt i svaret")
    new_reservations: int = field_with_meta(title="Antall nye reservasjoner", description="Oppsummert fra alle enkeltvise svar")
    new_reservation_removals: int = field_with_meta(title="Antall nye fjernede reservasjoner", description="Oppsummert fra alle enkeltvise svar")
    error_message_aes: str = field_with_meta(title="Feilmelding", description="Dersom det var en feilmelding i API-kallet legges den her", encrypted=True)