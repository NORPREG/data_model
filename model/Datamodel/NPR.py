from typing_extensions import Annotated
from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field

from typing import Optional, List, Literal
from datetime import datetime

from norpreg.Dataclasses.utils import field_with_meta


class NPR(BaseModel):    
    redcap_repeat_instance: str = Field('new', json_schema_extra={"transfer_only": True})
    redcap_repeat_instrument: str = Field('npr', json_schema_extra={"transfer_only": True})
    record_id: Optional[str] = Field(None, title="Pasientnøkkel i NORPREG", json_schema_extra={"transfer_only": True})

    InnDato: datetime = Field(None, title="Inn-dato", description="Tidspunkt for start av fraksjon")
    UtDato: datetime = Field(None, title="Ut-dato", description="Tidspunkt for slutt av fraksjon")
    Omsorg: Literal["3", "8"] = Field(None, title="Omsorgsnivå", description="Om pasienten er poliklinisk (3) eller inneliggende (8)") # 3 = Poliklinisk; 8 = Inneliggende
    Kno: str = Field(None, title="Kontakt ID", description="Unik identifikator for oppmøte / behandlingsfraksjon")
    Pkode: str = Field(None, title="Prosedyrekode", description="Følger NKPK (Norsk klinisk prosedyrekodeverk)")
    Intensjon: str = Field(None, title="Intensjon", description="Behandlingsintensjon, f.eks. kurativ eller palliativ")
    Machine: str = Field(None, title="Maskin ID", description="Unik identifikator for behandlingsmaskinen")
    RefVolumId: str = Field(None, title="Referansevolum ID")
    RefVolumNavn: str = Field(None, title="Referansevolum Navn")
    RegionKode: str = Field(None, title="Regionskode")
    RegionNavn: str = Field(None, title="Regionsnavn")
    PlanTotDose: str = Field(None, title="Totalt planlagt dose [Gy]", description="Til primært normeringsvolum")
    DoseKorr: str = Field(None, title="Dosekorreksjon [Gy]", description="Legges til ved rebestrålinger")
    DKMerknad: str = Field(None, title="Dosekorreksjon merknad")
    PlanDose: str = Field(None, title="Planlagt fraksjonsdose [Gy]", description="Til primært normeringsvolum")
    GittDose: str = Field(None, title="Gitt fraksjonsdose [Gy]", description="Til primært normeringsvolum")
    PlanUID: str = field_with_meta(None, title="Plan UID", description="Unik identifikator for behandlingsplanen -- SOP Instance UID", dicom="(0008,0018)")
    PIDno: str = Field(None, title="Pseudonymisert nøkkel i Aria", json_schema_extra={"document_only": True})
    PersNo: str = Field(None, title="Fødselsnummer", json_schema_extra={"document_only": True})
    Kjonn: Literal["1", "2"] = Field(None, title="Kjønn", description="1 = Mann, 2 = kvinne") # 1 mann, 2 kvinne
    Fodselsar: str = Field(None, title="Fødselsår", json_schema_extra={"document_only": True})
    Fodselsdato: str = Field(None, title="Fødselsdato")
    Komm: str = Field(None, title="Kommunenummer")
    Bydel: str = Field(None, title="Bydelsnummer", description="Kun relevant for Oslo")
    Hdiag: str = Field(None, title="Diagnosekode (ICD10)")
    NyPas: str = Field(None, title="Ny pasient", description="Indikerer om dette er første fraksjon for pasienten (1) eller ikke (0)")
    BehSerieId: str = Field(None, title="Behandlingsserie ID", description="Benyttes som global Course ID")
    BehSerieNavn: str = Field(None, title="Behandlingsserienavn")
    BehSerieStart: datetime = Field(None, title="Behandlingserie start")