from typing_extensions import Annotated
from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field

from typing import Optional, List, Literal
from datetime import datetime

from .utils import field_with_meta


class NPR(BaseModel):    
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('npr', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    InnDato: datetime = Field(title="Inn-dato", description="Tidspunkt for start av fraksjon")
    UtDato: datetime = Field(title="Ut-dato", description="Tidspunkt for slutt av fraksjon")
    Omsorg: Literal["3", "8"] = Field(title="Omsorgsnivå", description="Om pasienten er poliklinisk (3) eller inneliggende (8)") # 3 = Poliklinisk; 8 = Inneliggende
    Kno: str = Field(title="Kontakt ID", description="Unik identifikator for oppmøte / behandlingsfraksjon")
    Pkode: str = Field(title="Prosedyrekode", description="Følger NKPK (Norsk klinisk prosedyrekodeverk)")
    Intensjon: str = Field(title="Intensjon", description="Behandlingsintensjon, f.eks. kurativ eller palliativ")
    Machine: str = Field(title="Maskin ID", description="Unik identifikator for behandlingsmaskinen")
    RefVolumId: str = Field(title="Referansevolum ID")
    RefVolumNavn: str = Field(title="Referansevolum Navn")
    RegionKode: str = Field(title="Regionskode")
    RegionNavn: str = Field(title="Regionsnavn")
    PlanTotDose: str = Field(title="Totalt planlagt dose [Gy]", description="Til primært normeringsvolum")
    DoseKorr: str = Field(title="Dosekorreksjon [Gy]", description="Legges til ved rebestrålinger")
    DKMerknad: str = Field(title="Dosekorreksjon merknad")
    PlanDose: str = Field(title="Planlagt fraksjonsdose [Gy]", description="Til primært normeringsvolum")
    GittDose: str = Field(title="Gitt fraksjonsdose [Gy]", description="Til primært normeringsvolum")
    PlanUID: str = field_with_meta(title="Plan UID", description="Unik identifikator for behandlingsplanen -- SOP Instance UID", dicom="(0008,0018)")
    PIDno: str = Field(title="Pseudonymisert nøkkel i Aria", json_schema_extra={"document_only": True})
    PersNo: str = Field(title="Fødselsnummer", json_schema_extra={"document_only": True})
    Kjonn: Literal["1", "2"] = Field(title="Kjønn", description="1 = Mann, 2 = kvinne") # 1 mann, 2 kvinne
    Fodselsar: str = Field(title="Fødselsår", json_schema_extra={"document_only": True})
    Fodselsdato: str = Field(title="Fødselsdato")
    Komm: str = Field(title="Kommunenummer")
    Bydel: str = Field(title="Bydelsnummer", description="Kun relevant for Oslo")
    Hdiag: str = Field(title="Diagnosekode (ICD10)")
    NyPas: str = Field(title="Ny pasient", description="Indikerer om dette er første fraksjon for pasienten (1) eller ikke (0)")
    BehSerieId: str = Field(title="Behandlingsserie ID", description="Benyttes som global Course ID")
    BehSerieNavn: str = Field(title="Behandlingsserienavn")
    BehSerieStart: datetime = Field(title="Behandlingserie start")