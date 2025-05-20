from typing_extensions import Annotated

from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field
from typing import Optional, List, Literal
from datetime import datetime

def dicom_date_formatter(d: str) -> str:
	return datetime.strptime(d, "%Y%m%d").strftime("%Y-%m-%d")

def dicom_date_serializer(d: str) -> str:
	return datetime.strptime(d, "%Y%m%d").strftime("%Y-%m-%d")

def dicom_time_formatter(t: str) -> str:
	t_int = t.split(".")[0]
	return datetime.strptime(t_int, "%H%M%S").strftime("%H:%M:%S")

def dicom_time_serializer(t: str) -> str:
	t_int = t.split(".")[0]
	return datetime.strptime(t_int, "%H%M%S").strftime("%H:%M:%S")

DICOMDate = Annotated[
	str,
	BeforeValidator(dicom_date_formatter),
	PlainSerializer(dicom_date_serializer)
]

DICOMTime = Annotated[
	str,
	BeforeValidator(dicom_time_formatter),
	PlainSerializer(dicom_time_serializer)
]

def field_with_meta(title, description, default=None):
	# return Field(default=default, json_schema_extra={"title": title, "description": description})
	return Field(alias=title, description=description)

class DICOM(BaseModel):
	"""DICOM: Oversikt over DICOM-datasett"""
	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "dicom"

	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	dcm_course_id: Optional[str] = field_with_meta(title='DICOM Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')

	study_instance_uid: Optional[str] = field_with_meta(title='Study instance UID', description='Koblingsnøkkel mot DICOM-datasett på Study-nivå')
	study_description: Optional[str] = field_with_meta(title='Study description', description='Studiebeskrivelse fra DICOM-datasett på Study-nivå')
	import_datetime: Optional[datetime] = field_with_meta(title='Import datetime', description='Dato og tid for import av datasett i NORPREG')
	series_modality: Optional[str] = field_with_meta(title='Series modality', description='Modalitet for DICOM-datasett på Series-nivå')
	series_description: Optional[str] = field_with_meta(title='Series description', description='Seriebeskrivelse fra DICOM-datasett på Series-nivå')
	series_instance_uid: Optional[str] = field_with_meta(title='Series instance UID', description='Koblingsnøkkel mot DICOM-datasett på Series-nivå')
	files_nb: Optional[int] = field_with_meta(title='Files number', description='Antall filer i DICOM-datasett for enkelt Series')
	series_date: Optional[DICOMDate] = field_with_meta(title='Series date', description='Dato for DICOM-datasett på Series-nivå')
	station_name: Optional[str] = field_with_meta(title='Station name', description='Navn på enkeltmodalitet som har generert DICOM-datasett på Series-nivå')

class Fraction(BaseModel):
	"""Fraction: Oversikt over hver behandlingsfraksjon, som hentet fra RT Record"""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "fraction"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	fx_course_id: Optional[str] = field_with_meta(title='FK Fraction - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	fx_plan_uid: Optional[str] = field_with_meta(title='FK Fraction - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	treatment_machine_name: Optional[str] = field_with_meta(title='Treatment machine station name', description='Lokalt definert navn på behandlingsapparat')
	treatment_machine_model: Optional[str] = field_with_meta(title='Treatment machine model name', description='Modellnavn på behandlingsapparat')
	fx_dose_delivered: Optional[float] = field_with_meta(title='Fraction dose (delivered) [Gy]', description='Levert dose i Gy for denne behandlingsfraksjonen.')
	fx_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime', description='Dato og tid for behandlingsfraksjon')
	fx_number: Optional[int] = field_with_meta(title='Fraction number', description='Fraksjonsnummer (økende per fraksjon)')
	fx_mu_delivered: Optional[float] = field_with_meta(title='Fraction MUs delivered', description='Antall Monitor Units (MU) levert for denne behandlingsfraksjonen')
	fx_mu_planned: Optional[float] = field_with_meta(title='Fraction MUs planned', description='Antall Monitor Units (MU) planlagt for denne behandlingsfraksjonen')
	fx_time_delivered: Optional[float] = field_with_meta(title='Fraction time delivered [s]', description='Lengde i tid i sekunder for denne behandlingsfraksjonen')
	cumulative_dose_delivered: Optional[float] = field_with_meta(title='Cumulative dose delivered [Gy]', description='Kumulativ dose i Gy så langt for denne behandlingsplanen')
	termination_status: Optional[str] = field_with_meta(title='Termination status', description='Termineringsstatus for denne behandlingsfraksjonen')
	termination_code: Optional[str] = field_with_meta(title='Termination code', description='Termineringskode for denne behandlingsfraksjonen')
	verification_status: Optional[str] = field_with_meta(title='Verification status', description='Verifikasjonsstatus for denne behandlingsfraksjonen')
	fx_completion: Optional[float] = field_with_meta(title='Fraction completion', description='Hvor mye av dose til normeringsvolum er levert i henhold til planlagt i dennefraksjonen. Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)')

class Plan(BaseModel):
	"""Plan: Oversikt over en behandlingsplan. Inneholder både informasjon fra RT Plan-filen, men også fra RT Record for å beregne leverte doser"""

	#  redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "plan"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	plan_course_id: Optional[str] = field_with_meta(title='FK Plan - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	plan_uid: Optional[str] = field_with_meta(title='Plan SOP Instance UID', description='Denne RT Plan filens SOP Instance UID, brukes for å koble mot denne')

	ct_study_date: Optional[DICOMDate] = field_with_meta(title='CT Study date', description='Dato for Plan CT')
	plan_datetime: Optional[datetime] = field_with_meta(title='RT Plan datetime', description='Dato og tid for godkjent behandlingsplan')
	struct_datetime: Optional[datetime] = field_with_meta(title='RT Structure datetime', description='Dato og tid for inntegnede strukturer')
	dose_datetime: Optional[datetime] = field_with_meta(title='RT Dose datetime', description='Dato og tid for dosevolum')
	plan_label_raw: Optional[str] = field_with_meta(title='Plan label raw', description='Plannavn (label) som angitt hos OIS')
	plan_number: Optional[str] = field_with_meta(title='Plan number', description='Plannummer, NN eller NN.M, som tolket fra OIS. Angir behandlingsserie.replan') # parsed from plan raw label, can be 0x so str
	plan_name: Optional[str] = field_with_meta(title='Plan name', description='Plannavn uten plannummer')  # parsed from plan label
	total_dose_planned: Optional[float] = field_with_meta(title='Total dose planned [Gy]', description='Planlagt dose i Gy i denne behandlingsplanen. Hentet fra RT Plan')
	total_dose_delivered: Optional[float] = field_with_meta(title='Total dose delivered [Gy]', description='Levert dose i Gy i denne behandlingsplanen. Beregnet som summert dose til (primært) normeringsvolum i hver behandlingsfraksjon / RT Record')
	fx_dose_planned: Optional[float] = field_with_meta(title='Fraction dose planned [Gy]', description='Planlagt fraksjonsdose')
	fxs_planned: Optional[int] = field_with_meta(title='Number of fractions planned', description='Planlagt antall fraksjoner')
	fxs_delivered: Optional[int] = field_with_meta(title='Number of fractions delivered', description='Levert antall fraksjoner (fra tilhørende identifiserte behandlingsfraksjoner)')
	fx_delivered_from: Optional[int] = field_with_meta(title='Fraction number delivered from', description='Minste fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging')
	fx_delivered_to: Optional[int] = field_with_meta(title='Fraction number delivered to', description='Største fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging')
	fx_delivered_from_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime delivered from', description='Første fraksjonsdato funnet i denne behandlingsplanen')
	fx_delivered_to_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime delivered to', description='Siste fraksjonsdato funnet i denne behandlingsplanen')
	plan_completion: Optional[float] = field_with_meta(title='', description='Hvor mye av dose til normeringsvolum er levert i henhold til planlagt for hele behandlingsplanen. Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)')
	beam_count: Optional[int] = field_with_meta(title='Beam count', description='Antall behandlingsfelt i denne behandlingsplanen')
	patient_orientation: Optional[str] = field_with_meta(title='Patient orientation', description='Pasientens leie')
	tps_manufacturer: Optional[str] = field_with_meta(title='TPS manufacturer', description='Leverandør av programvare for behandlingsplan (TPS, Treatment Planning System)')
	tps_software_name: Optional[str] = field_with_meta(title='TPS software name', description='Navn på programvare for behandlingsplan (TPS, Treatment Planning System)')
	tps_software_version: Optional[str] = field_with_meta(title='TPS software version', description='Versjon av programvare for behandlingsplan (TPS, Treatment Planning System)')
	tx_modality: Optional[str] = field_with_meta(title='Treatment modality', description='Behandlingsmodalitet')
	tx_time: Optional[float] = field_with_meta(title='Treatment time', description='Behandlingstid, kun relevant for brakyterapi')
	total_mu: Optional[float] = field_with_meta(title='Total MUs', description='Totalt antall Monitor Units (MUs) for hele behandlingsplanen')
	dose_grid_res_x: Optional[float] = field_with_meta(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i X-retning, i mm')
	dose_grid_res_y: Optional[float] = field_with_meta(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i Y-retning, i mm')
	heterogeneity_correction: Optional[str] = field_with_meta(title='Heterogeneity correction', description='Heterogeneitetskorreksjon for doseberegning')
	complexity: Optional[float] = field_with_meta(title='Plan complexity', description='Young\'s plankompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1). MU-vektet sum av hver beams kompleksitet, som igjen er en MU-vektet sum av kontrollpunktenes kompleksitet.')
	

class DVH(BaseModel):
	"""DVH: Geometriske og dosimetriske data fra målvolum og behandlingsvolum"""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "structure"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	struct_course_id: Optional[str] = field_with_meta(title='FK Structure - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	struct_plan_uid: Optional[str] = field_with_meta(title='FK Structure - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')
	struct_uid: Optional[str] = field_with_meta(title='RT Structure SOP Instance UID', description='Denne RT Structure filens SOP Instance UID, brukes for å koble mot denne')
	ct_series_uid: Optional[str] = field_with_meta(title='CT Series UID', description='Koblingsnøkkel mot DICOM-datasett på Plan CT Series UID-nivå')

	is_dvh_plan_sum: Optional[bool] = field_with_meta(title='Is the DVH a plan-sum?', description='Beskriver underliggende struktur en enkelt plan eller hele behandlingsforløpet (for enkelt målvolum). Spesielt aktuell ved replan og plan-of-the-day. Aktuelle koblinger kan være Frame of Reference eller nummerering av plannavn') # = False
	mapped_roi_name: Optional[str] = field_with_meta(title='Mapped ROI name', description='Standardisert / mappet navn på struktur')
	roi_name: Optional[str] = field_with_meta(title='ROI name', description='Navn på struktur som angitt i TPS')
	roi_type: Optional[str] = field_with_meta(title='ROI type', description='Strukturtype')
	origin: Optional[str] = field_with_meta(title='Structure origin', description='Er strukturen inntegnet manuelt eller via AI-metoder?')
	origin_software: Optional[str] = field_with_meta(title='Structure delineation software', description='Programvare benyttet for automatisk inntegning')
	volume: Optional[float] = field_with_meta(title='Structure volume [cc]', description='Strukturvolum i cc, som beregnet fra struktursettet')
	min_dose: Optional[float] = field_with_meta(title='Voxelwise min dose [Gy]', description='Minste dose i Gy som beregnet fra struktursettet og RT dose')
	mean_dose: Optional[float] = field_with_meta(title='Voxelwise mean dose [Gy]', description='Gjennomsnittlig dose i Gy som beregnet fra struktursettet og RT dose')
	max_dose: Optional[float] = field_with_meta(title='Voxelwise max dose [Gy]', description='Største dose i Gy som beregnet fra struktursettet og RT dose')
	dvh_string: Optional[str] = field_with_meta(title='DVH string [compressed]', description='Hele DVH-strengen for strukturen, som beregnet fra struktursettet og RT dose. Teknisk: Lagret som en b64-kodet gzippet streng av bitpakkede uint16, hvor 10 000 angir 100 % volum, med statiske 0.1 Gy bins.')
	# roi_coord_string: Optional[str] = field_with_meta(title='ROI string [compressed]', description='Hele ROI-strengen for strukturen, sikkert noe komprimert. Ikke i bruk')
	dist_to_ptv_min: Optional[float] = field_with_meta(title='Min distance to PTV', description='Minste avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_mean: Optional[float] = field_with_meta(title='Mean distance to PTV', description='Gjennomsnittlig avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_median: Optional[float] = field_with_meta(title='Median distance to PTV', description='Median avstand avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_max: Optional[float] = field_with_meta(title='Max distance to PTV', description='Største avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_25: Optional[float] = field_with_meta(title='25th percentile distance to PTV', description='25. persentil for avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_75: Optional[float] = field_with_meta(title='75th percentile distance to PTV', description='75. persentil fo avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	scaling_factor: Optional[float] = field_with_meta(title='Dose scaling factor', description='Pålagt skaleringsfaktor for levert DVH-dose') # add to excel
	surface_area: Optional[float] = field_with_meta(title='ROI surface area [cm2]', description='Overflatearealet til strukturen gitt i cm2')
	ptv_overlap: Optional[float] = field_with_meta(title='PTV overlap [cc]', description='Volum for overlapp mellom aktuell struktur og (union) PTV, gitt i cc')
	centroid: Optional[str] = field_with_meta(title='ROI centroid [mm,mm,mm]', description='Sentroiden til aktuell struktur, gitt som 3-vektor streng i mm')
	dist_to_ptv_centroids: Optional[float] = field_with_meta(title='Distance to PTV centroid [cm]', description='Avstand mellom sentroider for aktuell struktur og (union) PTV')
	spread_x: Optional[float] = field_with_meta(title='Spread in X [cm]', description='Størrese i X-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	spread_y: Optional[float] = field_with_meta(title='Spread in Y [cm]', description='Størrese i Y-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	spread_z: Optional[float] = field_with_meta(title='Spread in Z [cm]', description='Størrese i Z-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	cross_section_max: Optional[float] = field_with_meta(title='Max cross section [cm2]', description='Største tverrsnitt for aktuell struktur over alle snitt [cm2]')
	cross_section_median: Optional[float] = field_with_meta(title='Median cross section [cm2]', description='Median tverrsnitt for aktuell struktur over alle snitt [cm2]')
	centroid_dist_to_iso_min: Optional[float] = field_with_meta(title='Centroid distance to isocenter min [cm]', description='Minste avstand mellom sentroide for aktuell struktur og isosenter (over alle felt) [cm]')
	centroid_dist_to_iso_max: Optional[float] = field_with_meta(title='Centroid distance to isocenter max [cm]', description='Største avstand mellom sentroide for aktuell struktur og isosenter (over alle felt) [cm]')
	integral_dose: Optional[float] = field_with_meta(title='Integral dose [cm3 Gy]', description='Integraldose til aktuell struktur i cm3 Gy, beregnet som gjennomsnittsdose * volum')
	color: Optional[str] = field_with_meta(title='ROI color', description='Farge til ROI som angitt i TPS')
	D2: Optional[float] = field_with_meta(title='D2 [Gy]', description='Dose i Gy til 2% av aktuell struktur')
	D10: Optional[float] = field_with_meta(title='D10% [Gy]', description='Dose i Gy til 10% av aktuell struktur')
	D20: Optional[float] = field_with_meta(title='D20% [Gy]', description='Dose i Gy til 20% av aktuell struktur')
	D30: Optional[float] = field_with_meta(title='D30% [Gy]', description='Dose i Gy til 30% av aktuell struktur')
	D40: Optional[float] = field_with_meta(title='D40% [Gy]', description='Dose i Gy til 40% av aktuell struktur')
	D50: Optional[float] = field_with_meta(title='D50% [Gy]', description='Dose i Gy til 50% av aktuell struktur')
	D60: Optional[float] = field_with_meta(title='D60% [Gy]', description='Dose i Gy til 60% av aktuell struktur')
	D70: Optional[float] = field_with_meta(title='D70% [Gy]', description='Dose i Gy til 70% av aktuell struktur')
	D80: Optional[float] = field_with_meta(title='D80% [Gy]', description='Dose i Gy til 80% av aktuell struktur')
	D90: Optional[float] = field_with_meta(title='D90% [Gy]', description='Dose i Gy til 90% av aktuell struktur')
	D98: Optional[float] = field_with_meta(title='D98% [Gy]', description='Dose i Gy til 98% av aktuell struktur ')
	D2cc: Optional[float] = field_with_meta(title='D2cc [Gy]', description='Dose i Gy til 2cc av aktuell struktur')
	V5Gy: Optional[float] = field_with_meta(title='V5Gy [%]', description='Volumet av aktuell struktur i % som mottar 5 Gy')
	V10Gy: Optional[float] = field_with_meta(title='V10Gy [%]', description='Volumet av aktuell struktur i % som mottar 10 Gy')
	V15Gy: Optional[float] = field_with_meta(title='V15Gy [%]', description='Volumet av aktuell struktur i % som mottar 15 Gy')
	V20Gy: Optional[float] = field_with_meta(title='V20Gy [%]', description='Volumet av aktuell struktur i % som mottar 20 Gy')
	V25Gy: Optional[float] = field_with_meta(title='V25Gy [%]', description='Volumet av aktuell struktur i % som mottar 25 Gy')
	V30Gy: Optional[float] = field_with_meta(title='V30Gy [%]', description='Volumet av aktuell struktur i % som mottar 30 Gy')
	V35Gy: Optional[float] = field_with_meta(title='V35Gy [%]', description='Volumet av aktuell struktur i % som mottar 35 Gy')
	V40Gy: Optional[float] = field_with_meta(title='V40Gy [%]', description='Volumet av aktuell struktur i % som mottar 40 Gy')
	V45Gy: Optional[float] = field_with_meta(title='V45Gy [%]', description='Volumet av aktuell struktur i % som mottar 45 Gy')
	V50Gy: Optional[float] = field_with_meta(title='V50Gy [%]', description='Volumet av aktuell struktur i % som mottar 50 Gy')
	V55Gy: Optional[float] = field_with_meta(title='V55Gy [%]', description='Volumet av aktuell struktur i % som mottar 55 Gy')
	V60Gy: Optional[float] = field_with_meta(title='V60Gy [%]', description='Volumet av aktuell struktur i % som mottar 60 Gy')
	V65Gy: Optional[float] = field_with_meta(title='V65Gy [%]', description='Volumet av aktuell struktur i % som mottar 65 Gy')
	V70Gy: Optional[float] = field_with_meta(title='V70Gy [%]', description='Volumet av aktuell struktur i % som mottar 70 Gy')
	V95: Optional[float] = field_with_meta(title='V95% [%]', description='Volumet av aktuell struktur i % som mottar 95% av planlagt dose til målvolum')

class DR(BaseModel):
	"""Dose Reference: Oversikt over normeringsvolum, både det primære som brukes som mål på fraksjonsdose og støtte-normeringsvolum"""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "dosereference"

	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')
	dr_course_id: Optional[str] = field_with_meta(title='FK Dose Reference - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	dr_plan_uid: Optional[str] = field_with_meta(title='FK Dose Reference - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	ref_dr_name: Optional[str] = field_with_meta(title='Referenced Dose Reference name', description='Navn på normeringsvolum')
	dr_type: Optional[str] = field_with_meta(title='Dose Reference structure type', description='Strukturtype på normeringsvolum (punkt, volum, ...)')
	dr_ref_type: Optional[str] = field_with_meta(title='Dose Reference type', description='Kategori av normeringsvolum (målvolum eller risikoorgan)')
	dr_dose_planned: Optional[float] = field_with_meta(title='Planned dose to Dose Reference [Gy]', description='Planlagt dose i Gy til normeringsvolum')
	dr_dose_delivered: Optional[float] = field_with_meta(title='Delivered dose to Dose Reference [Gy]', description='Levert dose i Gy til normeringsvolum, som summert fra behandlingsfraksjonene')
	dr_max_dose: Optional[float] = field_with_meta(title='Max dose to Dose Reference [Gy]', description='Største tillatt dose i Gy til normeringsvolum')
	dr_is_primary: Optional[bool] = field_with_meta(title='Is the Dose Reference primary', description="Er det primært normeringsvolum? -> Brukes til beregning av leverte doser")

class Beam(BaseModel):
	"""Beam: Informasjon om de ulike behandlingsfeltene"""
	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "beam"

	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')
	beam_course_id: Optional[str] = field_with_meta(title='FK Beam - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	beam_plan_uid: Optional[str] = field_with_meta(title='FK Beam - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	beam_tx_modality: Optional[str] = field_with_meta(title='Treatment modality', description='Behandlingsmodalitet tolket fra RTPlan.RadiationType. PHOTON, ELECTRON, NEUTRON, PROTON. Får 3D / arc modifikator dersom det er benyttet.')
	beam_number: Optional[int] = field_with_meta(title='Beam number', description='Tallangivelsen for dette feltet DICOM: (300A, 00C0)')
	beam_name: Optional[str] = field_with_meta(title='Beam name', description='Feltnavn, inneholder ofte vinkelinformasjon DICOM: (300A, 00C3) / (300A, 00C2)')
	fx_grp_number: Optional[int] = field_with_meta(title='Fraction group number', description='Gruppenummeret til fraksjonen (300A, 0071)')
	fx_count: Optional[int] = field_with_meta(title='Fraction count', description='Totalt antall fraksjoner for dette feltet (300A, 0078)')
	fx_grp_beam_count: Optional[int] = field_with_meta(title='Fraction group beam count', description='Antall felt i denne fraksjonsgruppen')
	beam_dose: Optional[float] = field_with_meta(title='Beam dose [Gy]', description='Planlagt dose for dette feltet i Gy (300A, 008B)')
	beam_mu: Optional[float] = field_with_meta(title='Beam Monitor Units', description='Antall Monitor Units (MUs) for dette feltet')
	radiation_type: Optional[str] = field_with_meta(title='Radiation type', description='Strålingstype for dette feltet (uten 3D modifikator) (300A, 00C6)')
	beam_energy_min: Optional[float] = field_with_meta(title='Min beam energy [MV / MeV]', description='Minste energi for strålefeltet. Enhet er MV for fotoner, MeV for protoner (300A, 0114)')
	beam_energy_max: Optional[float] = field_with_meta(title='Max beam energy [MV / MeV]', description='Største energi for strålefeltet. Enhet er MV for fotoner, MeV for protoner (300A, 0114)')
	beam_type: Optional[str] = field_with_meta(title='Beam type', description='Felttype, STATIC eller DYNAMIC (300A,00C4)')
	control_point_count: Optional[int] = field_with_meta(title='Control point count', description='Antall kontrollpunkter for dette feltet')
	gantry_start: Optional[float] = field_with_meta(title='Gantry start [deg]', description='Gantry startvinkel i grader (300A, 011E)')
	gantry_end: Optional[float] = field_with_meta(title='Gantry end [deg]', description='Gantry sluttvinkel i grader (300A, 011E)')
	gantry_rot_dir: Literal["CW", "CC", "NONE"] = field_with_meta(title='Gantry rotation direction', description='Retning til gantryrotasjon, CW / CC / NONE (300A, 011F)')
	gantry_range: Optional[float] = field_with_meta(title='Gantry range [deg]', description='Hvor mange grader gantry roterer (300A, 011E)')
	gantry_min: Optional[float] = field_with_meta(title='Gantry min [deg]', description='Minste gantryvinkel i grader (300A, 011E)')
	gantry_max: Optional[float] = field_with_meta(title='Gantry max [deg]', description='Største gantryvinkel i grader (300A, 011E)')
	collimator_start: Optional[float] = field_with_meta(title='Collimator start [deg]', description='Kollimator startvinkel i grader (300A, 0120)')
	collimator_end: Optional[float] = field_with_meta(title='Colimator end [deg]', description='Kollimator sluttvinkel i grader (300A, 0120)')
	collimator_rot_dir: Optional[str] = field_with_meta(title='Collimator rotation direction', description='Retning til kollimatorrotasjon, CW / CC / NONE (300A, 0121)')
	collimator_range: Optional[float] = field_with_meta(title='Collimator range [deg]', description='Hvor mange grader kollimator roterer (300A, 0120)')
	collimator_min: Optional[float] = field_with_meta(title='Collimator min [deg]', description='Minste kollimatorvinkel i grader (300A, 0120)')
	collimator_max: Optional[float] = field_with_meta(title='Collimator max [deg]', description='Største kollimatorvinkel i grader (300A, 0120)')
	# Check these below, (300A, 0120) is not couch angles and they (table top) are modelled differently
	couch_start: Optional[float] = field_with_meta(title='Couch start [deg]', description='Bord startvinkel i grader (300A, 0122)')
	couch_end: Optional[float] = field_with_meta(title='Cough end [deg]', description='Bord sluttvinkel i grader (300A, 0122)')
	couch_rot_dir: Optional[str] = field_with_meta(title='Cough rotation direction', description='Retning til bordrotasjon, CW / CC / NONE (300A, 0122)')
	couch_range: Optional[float] = field_with_meta(title='Cough range [deg]', description='Hvor mange grader bord roterer (300A, 0122)')
	couch_min: Optional[float] = field_with_meta(title='Cough min [deg]', description='Største bordvinkel i grader (300A, 0122)')
	couch_max: Optional[float] = field_with_meta(title='Cough max [deg]', description='Minste bordvinkel i grader (300A, 0122)')
	beam_dose_pt: Optional[str] = field_with_meta(title='Beam dose Specification point [Gy]', description='Dose til primært normeringsvolum i Gy for dette feltet (300A, 0082)')
	isocenter: Optional[str] = field_with_meta(title='Isocenter position', description='Isosenterposisjon i x,y,z cm (300A, 012C)')
	ssd: Optional[float] = field_with_meta(title='Source to surface distance', description='Avstand mellom kilde og overflate i cm. Gjennomsnitt om det er ARC (300A, 0130)')
	treatment_machine: Optional[str] = field_with_meta(title='Treatment machine name', description='(Lokalt) navn på behandlingsapparat (300A, 00B2)')
	scan_mode: Optional[str] = field_with_meta(title='Scan mode', description='Hvordan strålen scannes under behandling. NONE / UNIFORM / MODULATED / MODULATED_SPEC (300A, 0308)')
	scan_spot_count: Optional[int] = field_with_meta(title='Scan spot count', description='Hvor mange punkter som benyttes under spot scanning (300A, 0392)')
	beam_mu_per_deg: Optional[float] = field_with_meta(title='Beam MUs per degree', description='Hvor mange monitoreringsenheter per rotasjonsgrad')
	beam_mu_per_cp: Optional[float] = field_with_meta(title='Beam MUs per control point', description='Hvor mange monitoreringsenheter per kontrollpunkt')
	area_min: Optional[float] = field_with_meta(title='Area min [cm2]', description='Minste feltareal i cm2')
	area_mean: Optional[float] = field_with_meta(title='Area mean [cm2]', description='Gjennomsnittlig feltareal i cm2')
	area_median: Optional[float] = field_with_meta(title='Area median [cm2]', description='Median feltareal i cm2')
	area_max: Optional[float] = field_with_meta(title='Area max [cm2]', description='Største feltareal i cm2')
	perim_min: Optional[float] = field_with_meta(title='Beam perimeter min [cm]', description='Minste feltomkrets i cm')
	perim_mean: Optional[float] = field_with_meta(title='Beam perimeter mean [cm]', description='Gjennomsnittlig feltomkrets i cm')
	perim_median: Optional[float] = field_with_meta(title='Beam perimeter median [cm]', description='Median feltomkrets i cm')
	perim_max: Optional[float] = field_with_meta(title='Beam perimeter max [cm]', description='Største feltomkrets i cm')
	x_perim_min: Optional[float] = field_with_meta(title='Beam perimeter X min [cm]', description='Minste feltomkrets (X) i cm')
	x_perim_mean: Optional[float] = field_with_meta(title='Beam perimeter X mean [cm]', description='Gjennomsnittlig feltomkrets (X) i cm')
	x_perim_median: Optional[float] = field_with_meta(title='Beam perimeter X median [cm]', description='Median feltomkrets (X) i cm')
	x_perim_max: Optional[float] = field_with_meta(title='Beam perimeter X max [cm]', description='Største feltomkrets (X) i cm')
	y_perim_min: Optional[float] = field_with_meta(title='Beam perimeter Y min [cm]', description='Minste feltomkrets (Y) i cm')
	y_perim_mean: Optional[float] = field_with_meta(title='Beam perimeter Y mean [cm]', description='Gjennomsnittlig feltomkrets (Y) i cm')
	y_perim_median: Optional[float] = field_with_meta(title='Beam perimeter Y median [cm]', description='Median feltomkrets (Y) i cm')
	y_perim_max: Optional[float] = field_with_meta(title='Beam perimeter Y max [cm]', description='Største feltomkrets (Y) i cm')
	complexity_min: Optional[float] = field_with_meta(title='Field complexity min', description='Minste Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_mean: Optional[float] = field_with_meta(title='Field complexity mean', description='Gjennomsnittlig Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_median: Optional[float] = field_with_meta(title='Field complexity median', description='Median Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_max: Optional[float] = field_with_meta(title='Field complexity max', description='Største Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	cp_mu_min: Optional[float] = field_with_meta(title='Control point MU min', description='Lavest MU over alle kontrollpunktene')
	cp_mu_mean: Optional[float] = field_with_meta(title='Control point MU mean', description='Gjennomsnittlig MU over alle kontrollpunktene')
	cp_mu_median: Optional[float] = field_with_meta(title='Control point MU median', description='Median MU over alle kontrollpunktene')
	cp_mu_max: Optional[float] = field_with_meta(title='Control point MU max', description='Største MU over alle kontrollpunktene')
	beam_complexity: Optional[float] = field_with_meta(title='Beam complexity', description='Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1). MU-vektet sum av kontrollpunktenes kompleksitet.')