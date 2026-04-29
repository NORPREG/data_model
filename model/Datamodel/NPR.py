from typing_extensions import Annotated
from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field

from typing import Optional, List, Literal
from datetime import datetime, date

from .utils import field_with_meta


class NPR(BaseModel):    
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('npr', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    InnDato: datetime = Field(title="Inn-dato", description="Tidspunkt for start av fraksjon")
    UtDato: datetime = Field(title="Ut-dato", description="Tidspunkt for slutt av fraksjon")
    Omsorg: Literal["3", "8"] = Field(title="Omsorgsnivå", description="Poliklinisk eller inneliggende kontakt", terminology="FinnKode 8406")
    Kno: str = Field(title="Kontakt ID", description="Unik identifikator for oppmøte / behandlingsfraksjon")
    Pkode: str = Field(title="Prosedyrekode", description="Type behandling eller doseplanlegging", terminology="Norsk klinisk prosedyrekodeverk (FinnKode 7275)")
    Intensjon: Literal["Kurativ", "Palliativ", "Annet", "Ukjent"] = Field(title="Intensjon", description="Behandlingsintensjon", terminology="FinnKode 9186")
    Machine: str = Field(title="Maskin ID", description="Unik identifikator for behandlingsmaskinen")
    RefVolumNavn: str = Field(title="Referansevolum Navn", description="Denne samsvarer med primært normeringsvolum (Dose Reference)")
    RefVolumId: str = Field(title="Referansevolum ID", description="Unik identifikator for referansevolumet")
    RegionKode: str = Field(title="Regionskode", description="ID for anatomisk region angitt for stråleterapi", terminology="FinnKode 9184")
    RegionNavn: str = Field(title="Regionsnavn", description="Navn på anatomisk region angitt for stråleterapi", terminology="FinnKode 9184")
    PlanTotDose: str = Field(title="Totalt planlagt dose", unit="Gy", description="Til primært normeringsvolum")
    DoseKorr: str = Field(title="Dosekorreksjon", unit="Gy", description="Legges til ved rebestrålinger")
    DKMerknad: str = Field(title="Dosekorreksjon merknad")
    PlanDose: str = Field(title="Planlagt fraksjonsdose", unit="Gy", description="Til primært normeringsvolum")
    GittDose: str = Field(title="Gitt fraksjonsdose", unit="Gy", description="Til primært normeringsvolum")
    PlanUID: str = field_with_meta(title="Plan UID", description="Unik identifikator for behandlingsplanen, svarer til SOP Instance UID for RT PLAN", dicom="(0008,0018)")
    PIDno: str = Field(title="Pseudonymisert nøkkel i Aria", json_schema_extra={"document_only": True})
    PersNo: str = Field(title="Fødselsnummer", json_schema_extra={"document_only": True})
    Kjonn: Literal["0", "1", "2", "9"] = Field(title="Kjønn", description="Kjønn. 0 = Ukjent, 1 = Mann, 2 = Kvinne, 9 = Annet", terminology="FinnKode 3101")
    Fodselsar: str = Field(title="Fødselsår", json_schema_extra={"document_only": True})
    Fodselsdato: date = Field(title="Fødselsdato")
    Komm: str = Field(title="Kommunenummer")
    Bydel: str = Field(title="Bydelsnummer", description="Kun relevant for Oslo", terminology="FinnKode 3403")
    Hdiag: str = Field(title="Diagnosekode", terminology="ICD10")
    NyPas: str = Field(title="Ny pasient", description="Indikerer om dette er første fraksjon for pasienten (1) eller ikke (0)")
    BehSerieId: str = Field(title="Behandlingsserie ID", description="Fra OIS. Benyttes som global Course ID i NORPREG")
    BehSerieNavn: str = Field(title="Behandlingsserienavn")
    BehSerieStart: datetime = Field(title="Tid for start av behandlingserie")