from typing_extensions import Annotated

from pydantic import BaseModel, PlainSerializer, BeforeValidator
from Dataclasses import ConquestDataclass
from typing import Optional
from datetime import datetime

DICOMDate = Annotated[
	str,
	BeforeValidator(ConquestDataclass.dicom_date_formatter),
	PlainSerializer(ConquestDataclass.dicom_date_serializer)
]

DICOMTime = Annotated[
	str,
	BeforeValidator(ConquestDataclass.dicom_time_formatter),
	PlainSerializer(ConquestDataclass.dicom_time_serializer)
]

class REDCapDICOM(BaseModel):
	"""Up to date with RC"""
	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "dicom"
	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')

	dcm_course_id: Optional[str] = Field(title='DICOM Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')

	study_instance_uid: Optional[str] = Field(title='Study instance UID', description='Koblingsnøkkel mot DICOM-datasett på Study-nivå')
	study_description: Optional[str] = Field(title='Study description', description='Studiebeskrivelse fra DICOM-datasett på Study-nivå')
	import_datetime: Optional[datetime] = Field(title='Import datetime', description='Dato og tid for import av datasett i NORPREG')
	series_modality: Optional[str] = Field(title='Series modality', description='Modalitet for DICOM-datasett på Series-nivå')
	series_description: Optional[str] = Field(title='Series description', description='Seriebeskrivelse fra DICOM-datasett på Series-nivå')
	series_instance_uid: Optional[str] = Field(title='Series instance UID', description='Koblingsnøkkel mot DICOM-datasett på Series-nivå')
	files_nb: Optional[int] = Field(title='Files number', description='Antall filer i DICOM-datasett for enkelt Series')
	series_date: Optional[DICOMDate] = Field(title='Series date', description='Dato for DICOM-datasett på Series-nivå')
	station_name: Optional[str] = Field(title='Station name', description='Navn på enkeltmodalitet som har generert DICOM-datasett på Series-nivå')

class REDCapFraction(BaseModel):
	"""Up to date with RC"""

	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "fraction"
	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')

	fx_course_id: Optional[str] = Field(title='FK Fraction - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	fx_plan_uid: Optional[str] = Field(title='FK Fraction - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	treatment_machine_name: Optional[str] = Field(title='Treatment machine station name', description='Lokalt definert navn på behandlingsapparat')
	treatment_machine_model: Optional[str] = Field(title='Treatment machine model name', description='Modellnavn på behandlingsapparat')
	fx_dose_delivered: Optional[float] = Field(title='Fraction dose (delivered) [Gy]', description='Levert dose i Gy for denne behandlingsfraksjonen.')
	fx_datetime: Optional[datetime] = Field(title='Fraction datetime', description='Dato og tid for behandlingsfraksjon')
	fx_number: Optional[int] = Field(title='Fraction number', description='Fraksjonsnummer (økende per fraksjon)')
	fx_mu_delivered: Optional[float] = Field(title='Fraction MUs delivered', description='Antall Monitor Units (MU) levert for denne behandlingsfraksjonen')
	fx_mu_planned: Optional[float] = Field(title='Fraction MUs planned', description='Antall Monitor Units (MU) planlagt for denne behandlingsfraksjonen')
	fx_time_delivered: Optional[float] = Field(title='Fraction time delivered [s]', description='Lengde i tid i sekunder for denne behandlingsfraksjonen')
	cumulative_dose_delivered: Optional[float] = Field(title='Cumulative dose delivered [Gy]', description='Kumulativ dose i Gy så langt for denne behandlingsplanen')
	termination_status: Optional[str] = Field(title='Termination status', description='Termineringsstatus for denne behandlingsfraksjonen')
	termination_code: Optional[str] = Field(title='Termination code', description='Termineringskode for denne behandlingsfraksjonen')
	verification_status: Optional[str] = Field(title='Verification status', description='Verifikasjonsstatus for denne behandlingsfraksjonen')
	fx_completion: Optional[float] = Field(title='Fraction completion', description='Hvor mye av dose til normeringsvolum er levert i henhold til planlagt i dennefraksjonen. Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)')

class REDCapPlan(BaseModel):
	"""Up to date with RC"""

	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "plan"
	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')

	plan_course_id: Optional[str] = Field(title='FK Plan - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	plan_uid: Optional[str] = Field(title='Plan SOP Instance UID', description='Denne RT Plan filens SOP Instance UID, brukes for å koble mot denne')

	ct_study_date: Optional[DICOMDate] = Field(title='CT Study date', description='Dato for Plan CT')
	plan_datetime: Optional[datetime] = Field(title='RT Plan datetime', description='Dato og tid for godkjent behandlingsplan')
	struct_datetime: Optional[datetime] = Field(title='RT Structure datetime', description='Dato og tid for inntegnede strukturer')
	dose_datetime: Optional[datetime] = Field(title='RT Dose datetime', description='Dato og tid for dosevolum')
	plan_label_raw: Optional[str] = Field(title='Plan label raw', description='Plannavn (label) som angitt hos OIS')
	plan_number: Optional[str] = Field(title='Plan number', description='Plannummer, NN eller NN.M, som tolket fra OIS. Angir behandlingsserie.replan') # parsed from plan raw label, can be 0x so str
	plan_name: Optional[str] = Field(title='Plan name', description='Plannavn uten plannummer')  # parsed from plan label
	total_dose_planned: Optional[float] = Field(title='Total dose planned [Gy]', description='Planlagt dose i Gy i denne behandlingsplanen. Hentet fra RT Plan')
	total_dose_delivered: Optional[float] = Field(title='Total dose delivered [Gy]', description='Levert dose i Gy i denne behandlingsplanen. Beregnet som summert dose til (primært) normeringsvolum i hver behandlingsfraksjon / RT Record')
	fx_dose_planned: Optional[float] = Field(title='Fraction dose planned [Gy]', description='Planlagt fraksjonsdose')
	fxs_planned: Optional[int] = Field(title='Number of fractions planned', description='Planlagt antall fraksjoner')
	fxs_delivered: Optional[int] = Field(title='Number of fractions delivered', description='Levert antall fraksjoner (fra tilhørende identifiserte behandlingsfraksjoner)')
	fx_delivered_from: Optional[int] = Field(title='Fraction number delivered from', description='Minste fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging')
	fx_delivered_to: Optional[int] = Field(title='Fraction number delivered to', description='Største fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging')
	fx_delivered_from_datetime: Optional[datetime] = Field(title='Fraction datetime delivered from', description='Første fraksjonsdato funnet i denne behandlingsplanen')
	fx_delivered_to_datetime: Optional[datetime] = Field(title='Fraction datetime delivered to', description='Siste fraksjonsdato funnet i denne behandlingsplanen')
	plan_completion: Optional[float] = Field(title='', description='Hvor mye av dose til normeringsvolum er levert i henhold til planlagt for hele behandlingsplanen. Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)')
	beam_count: Optional[int] = Field(title='Beam count', description='Antall behandlingsfelt i denne behandlingsplanen')
	patient_orientation: Optional[str] = Field(title='Patient orientation', description='Pasientens leie')
	tps_manufacturer: Optional[str] = Field(title='TPS manufacturer', description='Leverandør av programvare for behandlingsplan (TPS, Treatment Planning System)')
	tps_software_name: Optional[str] = Field(title='TPS software name', description='Navn på programvare for behandlingsplan (TPS, Treatment Planning System)')
	tps_software_version: Optional[str] = Field(title='TPS software version', description='Versjon av programvare for behandlingsplan (TPS, Treatment Planning System)')
	tx_modality: Optional[str] = Field(title='Treatment modality', description='Behandlingsmodalitet')
	tx_time: Optional[float] = Field(title='Treatment time', description='Behandlingstid, kun relevant for brakyterapi')
	total_mu: Optional[float] = Field(title='Total MUs', description='Totalt antall Monitor Units (MUs) for hele behandlingsplanen')
	dose_grid_res_x: Optional[float] = Field(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i X-retning, i mm')
	dose_grid_res_y: Optional[float] = Field(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i Y-retning, i mm')
	heterogeneity_correction: Optional[str] = Field(title='Heterogeneity correction', description='Heterogeneitetskorreksjon for doseberegning')
	complexity: Optional[float] = Field(title='Plan complexity', description='Young\'s plankompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1). MU-vektet sum av hver beams kompleksitet, som igjen er en MU-vektet sum av kontrollpunktenes kompleksitet.')
	

class REDCapDVH(BaseModel):
	"""Up to date with RC"""

	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "structure"
	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')

	struct_course_id: Optional[str] = Field(title='FK Structure - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	struct_plan_uid: Optional[str] = Field(title='FK Structure - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')
	struct_uid: Optional[str] = Field(title='RT Structure SOP Instance UID', description='Denne RT Structure filens SOP Instance UID, brukes for å koble mot denne')
	ct_series_uid: Optional[str] = Field(title='CT Series UID', description='Koblingsnøkkel mot DICOM-datasett på Plan CT Series UID-nivå')

	is_dvh_plan_sum: Optional[bool] = Field(title='Is the DVH a plan-sum?', description='Beskriver underliggende struktur en enkelt plan eller hele behandlingsforløpet (for enkelt målvolum). Spesielt aktuell ved replan og plan-of-the-day. Aktuelle koblinger kan være Frame of Reference eller nummerering av plannavn') # = False
	mapped_roi_name: Optional[str] = Field(title='Mapped ROI name', description='Standardisert / mappet navn på struktur')
	roi_name: Optional[str] = Field(title='ROI name', description='Navn på struktur som angitt i TPS')
	roi_type: Optional[str] = Field(title='ROI type', description='Strukturtype')
	origin: Optional[str] = Field(title='Structure origin', description='Er strukturen inntegnet manuelt eller via AI-metoder?')
	origin_software: Optional[str] = Field(title='Structure delineation software', description='Programvare benyttet for automatisk inntegning')
	volume: Optional[float] = Field(title='Structure volume [cc]', description='Strukturvolum i cc, som beregnet fra struktursettet')
	min_dose: Optional[float] = Field(title='Voxelwise min dose [Gy]', description='Minste dose i Gy som beregnet fra struktursettet og RT dose')
	mean_dose: Optional[float] = Field(title='Voxelwise mean dose [Gy]', description='Gjennomsnittlig dose i Gy som beregnet fra struktursettet og RT dose')
	max_dose: Optional[float] = Field(title='Voxelwise max dose [Gy]', description='Største dose i Gy som beregnet fra struktursettet og RT dose')
	dvh_string: Optional[str] = Field(title='DVH string [compressed]', description='Hele DVH-strengen for strukturen, som beregnet fra struktursettet og RT dose. Teknisk: Lagret som en b64-kodet gzippet streng av bitpakkede uint16, hvor 10 000 angir 100 % volum, med statiske 0.1 Gy bins.')
	# roi_coord_string: Optional[str] = Field(title='ROI string [compressed]', description='Hele ROI-strengen for strukturen, sikkert noe komprimert. Ikke i bruk')
	dist_to_ptv_min: Optional[float] = Field(title='Min distance to PTV', description='Minste avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_mean: Optional[float] = Field(title='Mean distance to PTV', description='Gjennomsnittlig avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_median: Optional[float] = Field(title='Median distance to PTV', description='Median avstand avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_max: Optional[float] = Field(title='Max distance to PTV', description='Største avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_25: Optional[float] = Field(title='25th percentile distance to PTV', description='25. persentil for avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	dist_to_ptv_75: Optional[float] = Field(title='75th percentile distance to PTV', description='75. persentil fo avstand mellom konturene for aktuell struktur og (union) PTV [mm]')
	scaling_factor: Optional[float] = Field(title='Dose scaling factor', description='Pålagt skaleringsfaktor for levert DVH-dose') # add to excel
	surface_area: Optional[float] = Field(title='ROI surface area [cm2]', description='Overflatearealet til strukturen gitt i cm2')
	ptv_overlap: Optional[float] = Field(title='PTV overlap [cc]', description='Volum for overlapp mellom aktuell struktur og (union) PTV, gitt i cc')
	centroid: Optional[str] = Field(title='ROI centroid [mm,mm,mm]', description='Sentroiden til aktuell struktur, gitt som 3-vektor streng i mm')
	dist_to_ptv_centroids: Optional[float] = Field(title='Distance to PTV centroid [cm]', description='Avstand mellom sentroider for aktuell struktur og (union) PTV')
	spread_x: Optional[float] = Field(title='Spread in X [cm]', description='Størrese i X-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	spread_y: Optional[float] = Field(title='Spread in Y [cm]', description='Størrese i Y-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	spread_z: Optional[float] = Field(title='Spread in Z [cm]', description='Størrese i Z-retning på rektangulær prisme som dekker aktuell struktur [cm]')
	cross_section_max: Optional[float] = Field(title='Max cross section [cm2]', description='Største tverrsnitt for aktuell struktur over alle snitt [cm2]')
	cross_section_median: Optional[float] = Field(title='Median cross section [cm2]', description='Median tverrsnitt for aktuell struktur over alle snitt [cm2]')
	centroid_dist_to_iso_min: Optional[float] = Field(title='Centroid distance to isocenter min [cm]', description='Minste avstand mellom sentroide for aktuell struktur og isosenter (over alle felt) [cm]')
	centroid_dist_to_iso_max: Optional[float] = Field(title='Centroid distance to isocenter max [cm]', description='Største avstand mellom sentroide for aktuell struktur og isosenter (over alle felt) [cm]')
	integral_dose: Optional[float] = Field(title='Integral dose [cm3 Gy]', description='Integraldose til aktuell struktur i cm3 Gy, beregnet som gjennomsnittsdose * volum')
	color: Optional[str] = Field(title='ROI color', description='Farge til ROI som angitt i TPS')
	D2: Optional[float] = Field(title='D2 [Gy]', description='Dose i Gy til 2\% av aktuell struktur')
	D10: Optional[float] = Field(title='D10% [Gy]', description='Dose i Gy til 10\% av aktuell struktur')
	D20: Optional[float] = Field(title='D20% [Gy]', description='Dose i Gy til 20\% av aktuell struktur')
	D30: Optional[float] = Field(title='D30% [Gy]', description='Dose i Gy til 30\% av aktuell struktur')
	D40: Optional[float] = Field(title='D40% [Gy]', description='Dose i Gy til 40\% av aktuell struktur')
	D50: Optional[float] = Field(title='D50% [Gy]', description='Dose i Gy til 50\% av aktuell struktur')
	D60: Optional[float] = Field(title='D60% [Gy]', description='Dose i Gy til 60\% av aktuell struktur')
	D70: Optional[float] = Field(title='D70% [Gy]', description='Dose i Gy til 70\% av aktuell struktur')
	D80: Optional[float] = Field(title='D80% [Gy]', description='Dose i Gy til 80\% av aktuell struktur')
	D90: Optional[float] = Field(title='D90% [Gy]', description='Dose i Gy til 90\% av aktuell struktur')
	D98: Optional[float] = Field(title='D98% [Gy]', description='Dose i Gy til 98\% av aktuell struktur ')
	D2cc: Optional[float] = Field(title='D2cc [Gy]', description='Dose i Gy til 2cc av aktuell struktur')
	V5Gy: Optional[float] = Field(title='V5Gy [%]', description='Volumet av aktuell struktur i \% som mottar 5 Gy')
	V10Gy: Optional[float] = Field(title='V10Gy [%]', description='Volumet av aktuell struktur i \% som mottar 10 Gy')
	V15Gy: Optional[float] = Field(title='V15Gy [%]', description='Volumet av aktuell struktur i \% som mottar 15 Gy')
	V20Gy: Optional[float] = Field(title='V20Gy [%]', description='Volumet av aktuell struktur i \% som mottar 20 Gy')
	V25Gy: Optional[float] = Field(title='V25Gy [%]', description='Volumet av aktuell struktur i \% som mottar 25 Gy')
	V30Gy: Optional[float] = Field(title='V30Gy [%]', description='Volumet av aktuell struktur i \% som mottar 30 Gy')
	V35Gy: Optional[float] = Field(title='V35Gy [%]', description='Volumet av aktuell struktur i \% som mottar 35 Gy')
	V40Gy: Optional[float] = Field(title='V40Gy [%]', description='Volumet av aktuell struktur i \% som mottar 40 Gy')
	V45Gy: Optional[float] = Field(title='V45Gy [%]', description='Volumet av aktuell struktur i \% som mottar 45 Gy')
	V50Gy: Optional[float] = Field(title='V50Gy [%]', description='Volumet av aktuell struktur i \% som mottar 50 Gy')
	V55Gy: Optional[float] = Field(title='V55Gy [%]', description='Volumet av aktuell struktur i \% som mottar 55 Gy')
	V60Gy: Optional[float] = Field(title='V60Gy [%]', description='Volumet av aktuell struktur i \% som mottar 60 Gy')
	V65Gy: Optional[float] = Field(title='V65Gy [%]', description='Volumet av aktuell struktur i \% som mottar 65 Gy')
	V70Gy: Optional[float] = Field(title='V70Gy [%]', description='Volumet av aktuell struktur i \% som mottar 70 Gy')
	V95: Optional[float] = Field(title='V95% [%]', description='Volumet av aktuell struktur i \% som mottar 95\% av planlagt dose til målvolum')

class REDCapDR(BaseModel):
	"""Up to date with RC"""

	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "dosereference"

	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')
	dr_course_id: Optional[str] = Field(title='FK Dose Reference - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	dr_plan_uid: Optional[str] = Field(title='FK Dose Reference - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	ref_dr_name: Optional[str] = Field(title='Referenced Dose Reference name', description='Navn på normeringsvolum')
	dr_type: Optional[str] = Field(title='Dose Reference structure type', description='Strukturtype på normeringsvolum (punkt, volum, ...)')
	dr_ref_type: Optional[str] = Field(title='Dose Reference type', description='Kategori av normeringsvolum (målvolum eller risikoorgan)')
	dr_dose_planned: Optional[float] = Field(title='Planned dose to Dose Reference [Gy]', description='Planlagt dose i Gy til normeringsvolum')
	dr_dose_delivered: Optional[float] = Field(title='Delivered dose to Dose Reference [Gy]', description='Levert dose i Gy til normeringsvolum, som summert fra behandlingsfraksjonene')
	dr_max_dose: Optional[float] = Field(title='Max dose to Dose Reference [Gy]', description='Største tillatt dose i Gy til normeringsvolum')
	dr_is_primary: Optional[bool] = Field(title='Is the Dose Reference primary', description="Er det primært normeringsvolum? -> Brukes til beregning av leverte doser")

class REDCapBeam(BaseModel):
	"""Up to date with RC"""
	redcap_repeat_instance: str = 'new'
	redcap_repeat_instrument: str = "beam"

	record_id: Optional[str] = Field(title='Løpenummer i NORPREG', description='Angis automatisk for hver pasient')
	beam_course_id: Optional[str] = Field(title='', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	beam_plan_uid: Optional[str] = Field(title='', description='')

	beam_tx_modality: Optional[str] = Field(title='', description='')
	beam_number: Optional[int] = Field(title='', description='')
	beam_name: Optional[str] = Field(title='', description='')
	fx_grp_number: Optional[int] = Field(title='', description='')
	fx_count: Optional[int] = Field(title='', description='')
	fx_grp_beam_count: Optional[int] = Field(title='', description='')
	beam_dose: Optional[float] = Field(title='', description='')
	beam_mu: Optional[float] = Field(title='', description='')
	radiation_type: Optional[str] = Field(title='', description='')
	beam_energy_min: Optional[float] = Field(title='', description='')
	beam_energy_max: Optional[float] = Field(title='', description='')
	beam_type: Optional[str] = Field(title='', description='')
	control_point_count: Optional[int] = Field(title='', description='')
	gantry_start: Optional[float] = Field(title='', description='')
	gantry_end: Optional[float] = Field(title='', description='')
	gantry_rot_dir: Optional[str] = Field(title='', description='')
	gantry_range: Optional[float] = Field(title='', description='')
	gantry_min: Optional[float] = Field(title='', description='')
	gantry_max: Optional[float] = Field(title='', description='')
	collimator_start: Optional[float] = Field(title='', description='')
	collimator_end: Optional[float] = Field(title='', description='')
	collimator_rot_dir: Optional[str] = Field(title='', description='')
	collimator_range: Optional[float] = Field(title='', description='')
	collimator_min: Optional[float] = Field(title='', description='')
	collimator_max: Optional[float] = Field(title='', description='')
	couch_start: Optional[float] = Field(title='', description='')
	couch_end: Optional[float] = Field(title='', description='')
	couch_rot_dir: Optional[str] = Field(title='', description='')
	couch_range: Optional[float] = Field(title='', description='')
	couch_min: Optional[float] = Field(title='', description='')
	couch_max: Optional[float] = Field(title='', description='')
	beam_dose_pt: Optional[str] = Field(title='', description='')
	isocenter: Optional[str] = Field(title='', description='')
	ssd: Optional[float] = Field(title='', description='')
	treatment_machine: Optional[str] = Field(title='', description='')
	scan_mode: Optional[str] = Field(title='', description='')
	scan_spot_count: Optional[int] = Field(title='', description='')
	beam_mu_per_deg: Optional[float] = Field(title='', description='')
	beam_mu_per_cp: Optional[float] = Field(title='', description='')
	area_min: Optional[float] = Field(title='', description='')
	area_mean: Optional[float] = Field(title='', description='')
	area_median: Optional[float] = Field(title='', description='')
	area_max: Optional[float] = Field(title='', description='')
	perim_min: Optional[float] = Field(title='', description='')
	perim_mean: Optional[float] = Field(title='', description='')
	perim_median: Optional[float] = Field(title='', description='')
	perim_max: Optional[float] = Field(title='', description='')
	x_perim_min: Optional[float] = Field(title='', description='')
	x_perim_mean: Optional[float] = Field(title='', description='')
	x_perim_median: Optional[float] = Field(title='', description='')
	x_perim_max: Optional[float] = Field(title='', description='')
	y_perim_min: Optional[float] = Field(title='', description='')
	y_perim_mean: Optional[float] = Field(title='', description='')
	y_perim_median: Optional[float] = Field(title='', description='')
	y_perim_max: Optional[float] = Field(title='', description='')
	complexity_min: Optional[float] = Field(title='', description='')
	complexity_mean: Optional[float] = Field(title='', description='')
	complexity_median: Optional[float] = Field(title='', description='')
	complexity_max: Optional[float] = Field(title='', description='')
	cp_mu_min: Optional[float] = Field(title='', description='')
	cp_mu_mean: Optional[float] = Field(title='', description='')
	cp_mu_median: Optional[float] = Field(title='', description='')
	cp_mu_max: Optional[float] = Field(title='', description='')
	beam_complexity: Optional[float] = Field(title='', description='')
