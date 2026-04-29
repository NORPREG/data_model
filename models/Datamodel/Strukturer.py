from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field

from .utils import field_with_meta

class Plan(BaseModel):
    """Parquet storage for array data
    
    Contains
    * Plan-wide metadata (year / uid / name / HF)
    * Lists of structure names and types
    * Nested lists of DVH / ROI arrays"""

    hf: Optional[str] = field_with_meta(title="Helseforetak", description="Hvilken KREST-XXX dataene tilhører")
    pseudo_key: Optional[str] = field_with_meta(title="Koblingsnøkkel i NORPREG", description="Angis automatisk for hver pasient. Format er 7-karakter heksadesimal (f.eks. a72bf40).")
    plan_year: Optional[int] = field_with_meta(title="År for doseplan", description="År (YYYY) for doseplan (Study Date)", dicom="(0008, 0051)")
    plan_uid: Optional[str] = field_with_meta(title="Plan UID", description="SOP Instance UID for RT PLAN objektet, brukes som kobling")
    plan_name: Optional[str] = field_with_meta(title="Plan name", description="Beskrivelse av doseplanen", dicom="(300A,0002)")

    structure_names: List[str] = field_with_meta(title="Strukturnavn", description="Navn på gjeldende struktur, fra RT Structure", dicom="(3006,0026)")
    structure_types: List[str] = field_with_meta(title="Strukturtype", description="Type på gjelende struktur (organ, PTV, ...), fra RT Structure", dicom="(3006,00A4)")
    structure_volumes: List[float] = field_with_meta(title="Strukturvolum [cc]", description="Beregnet fra koordinatene med dicompyler")
    dose_calc_sec: List[float] = field_with_meta(title="Doseberegningstid", description="Hvor lang tid for hele doseberegningen. Avhengig av algoritme: Små strukturer interpoleres mer.")

    dvh_relative_volumes_nested: List[List[float]] = field_with_meta(title="DVH: vektor med relative volumer", description="Volumene går fra (0...1). Må sees i sammenheng med dvh_doses_gy_nested. Beregnet med dicompyler.")
    dvh_doses_gy_nested: List[List[float]] = field_with_meta(title="DVH: vektor med dose [Gy]", description="Doseakse med bincenter-verdier, fra 0.05 Gy, 0.15 Gy, ... til Dmax for angitt struktur. Må sees i sammenheng med dvh_relative_volumes_nested. Beregned med dicompyler.")
    
    roi_coords_x_mm_nested: List[List[float]] = field_with_meta(title="ROI: Vektor med X-koordinater", description="Endimensjonal vektor med alle X-koordinatene, må sees i sammenheng med Y,Z. Oppløsningen er angitt i RT Structure.")
    roi_coords_y_mm_nested: List[List[float]] = field_with_meta(title="ROI: Vektor med Y-koordinater", description="Endimensjonal vektor med alle Y-koordinatene, må sees i sammenheng med X,Z. Oppløsningen er angitt i RT Structure.")
    roi_coords_z_mm_nested: List[List[float]] = field_with_meta(title="ROI: Vektor med Z-koordinater", description="Endimensjonal vektor med alle Z-koordinatene, må sees i sammenheng med X,Y. Oppløsningen er angitt i RT Structure (= struktur-snittykkelse).")
    roi_coords_offsets_nested: List[List[float]] = field_with_meta(title="ROI: Vektor med Z-offsets", description="Hvert element angir hvor hver nye Z-koordinat begynner i x,y,z ROI-listene")