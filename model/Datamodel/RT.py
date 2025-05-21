from typing_extensions import Annotated

from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field
from typing import Optional, List, Literal
from datetime import datetime

from .utils import field_with_meta

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

roi_types = ("EXTERNAL", "PTV", "CTV", "GTV", "TREATED_VOLUME", "IRRAD_VOLUME","OAR", "BOLUS", "AVOIDANCE", "ORGAN",
			"MARKER", "REGISTRATION", "ISOCENTER", "CONTRAST_AGENT", "CAVITY", "BRACHY_CHANNEL", "BRACHY_ACCESSORY", 
			"BRACHY_SRC_APP", "SUPPORT", "FIXATION", "DOSE_REGION", "CONTROL", "DOSE_MEASUREMENT")

patient_orientations_dict = {
	"HFP": "Head First-Prone",
	"HFS": "Head First-Supine",
	"HFDR": "Head First-Decubitus Right",
	"HFDL": "Head First-Decubitus Left",
	"FFDR": "Feet First-Decubitus Right",
	"FFDL": "Feet First-Decubitus Left",
	"FFP": "Feet First-Prone",
	"FFS": "Feet First-Supine",
	"LFP": "Left First-Prone",
	"LFS": "Left First-Supine",
	"RFP": "Right First-Prone",
	"RFS": "Right First-Supine",
	"AFDR": "Anterior First-Decubitus Right",
	"AFDL": "Anterior First-Decubitus Left",
	"PFDR": "Posterior First-Decubitus Right",
	"PFDL": "Posterior First-Decubitus Left"
}
patient_orientations_tuple = tuple(patient_orientations_dict.keys())
patient_orientations_descr = [ f"{k}: {v}" for k,v in patient_orientations_dict.items()]

class DICOM(BaseModel):
	"""Oversikt over DICOM-datasett
	   ============================
	
	"""
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
	"""Oversikt over hver behandlingsfraksjon
	   ======================================
	
		Som hentet fra RT Record, og samkjørt med NPR-rapporten. For Mosaiq-systemer er det NPR-rapporten som er primærkilden."""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "fraction"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	fx_course_id: Optional[str] = field_with_meta(title='FK Fraction - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	fx_plan_uid: Optional[str] = field_with_meta(title='FK Fraction - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	treatment_machine_name: Optional[str] = field_with_meta(title='Treatment machine station name', description='Lokalt definert navn på behandlingsapparat', dicom="(300A,00B2)")
	treatment_machine_manufacturer: Optional[str] = field_with_meta(title='Treatment machine manufacturer', description='Leverandør av behandlingsapparat', dicom="(0008,0070)") # ADD THIS SOMEWHERE
	treatment_machine_model: Optional[str] = field_with_meta(title='Treatment machine model name', description='Modellnavn på behandlingsapparat', dicom="(0008,1090)")
	fx_dose_delivered: Optional[float] = field_with_meta(title='Fraction dose (delivered) [Gy]', description='Levert dose for denne behandlingsfraksjonen. Summert BeamDose til primært normeringsvolum', unit="Gy", dicom="(300A,0084)")
	fx_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime', description='Dato og tid for behandlingsfraksjon', dicom="(3008,0250)")
	fx_number: Optional[int] = field_with_meta(title='Fraction number', description='Fraksjonsnummer (økende per fraksjon)', dicom="(3008,0022)")
	fx_mu_delivered: Optional[float] = field_with_meta(title='Fraction MUs delivered', description='Antall Monitor Units (MU) levert for denne behandlingsfraksjonen. Summert for hvert kontrollpunt', dicom="(3008,0044)")
	fx_mu_planned: Optional[float] = field_with_meta(title='Fraction MUs planned', description='Antall Monitor Units (MU) planlagt for denne behandlingsfraksjonen. Summert for hvert kontrollpunt', dicom="(3008,0042)")
	fx_time_delivered: Optional[float] = field_with_meta(title='Fraction time delivered [s]', description='Lengde i tid i sekunder for denne behandlingsfraksjonen. Summert fra tiden for hvert leverte felt', unit="s", dicom="(3008,003B)")
	cumulative_dose_delivered: Optional[float] = field_with_meta(title='Cumulative dose delivered [Gy]', description='Kumulativ dose så langt for denne behandlingsplanen. Summert BeamDose til primært normeringsvolum i hver RT Record', unit="Gy", dicom="(300A,0084)")
	termination_status: Optional[Literal["NORMAL", "OPERATOR", "MACHINE", "UNKNOWN"]] = \
		field_with_meta(title='Termination status', description='Termineringsstatus for denne behandlingsfraksjonen', values=["NORMAL", "OPERATOR", "MACHINE", "UNKNOWN"], dicom="(3008,002A)")
	# termination_code: Optional[str] = field_with_meta(title='Termination code', description='Termineringskode for denne behandlingsfraksjonen')

	# Treatment Termination Code (3008,002B) was previously included in this Module but has been retired. 
	# See PS3.3-2023a. The RT Treatment Termination Reason Code Sequence (300A,0715) and 
	# Machine-Specific Treatment Termination Code Sequence (300A,0716) should be used for machine readable codes 
	# and Treatment Termination Description (300A,0730) for human readable text respectively.

	verification_status: Optional[Literal["VERIFIED", "VERIFIED_OVR", "NOT_VERIFIED"]] = \
		field_with_meta(title='Verification status', description='Verifikasjonsstatus for denne behandlingsfraksjonen', dicom="(3008,002C)", 
		values=[
			"VERIFIED: treatment verified", 
			"VERIFIED_OVR: treatment verified with at least one out-of-range value overridden",
			"NOT_VERIFIED: treatment verified manually"]
	)

	fx_completion: Optional[float] = field_with_meta(title='Fraction completion', 
		description="Hvor mye av dose til normeringsvolum er levert i henhold til planlagt i denne fraksjonen."
					" Den er beregnet som levert dose til primært normeringsvolum fra RT Records / planlagt dose til primært normeringsvolum "
					"Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)")

class Plan(BaseModel):
	"""Oversikt over en behandlingsplan
	   ================================
	   
	   Inneholder både informasjon fra RT Plan-filen, men også fra RT Record for å beregne leverte doser"""

	#  redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "plan"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	plan_course_id: Optional[str] = field_with_meta(title='FK Plan - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	plan_uid: Optional[str] = field_with_meta(title='Plan SOP Instance UID', description='Denne RT Plan filens SOP Instance UID, brukes for å koble mot denne')

	ct_study_date: Optional[DICOMDate] = field_with_meta(title='CT Study date', description='Dato for Plan CT', dicom="(0008, 0020)")
	plan_datetime: Optional[datetime] = field_with_meta(title='RT Plan datetime', description='Dato og tid for godkjent behandlingsplan', dicom="(300A, 0006)")
	struct_datetime: Optional[datetime] = field_with_meta(title='RT Structure datetime', description='Dato og tid for inntegnede strukturer', dicom="(3006, 0008)")
	dose_datetime: Optional[datetime] = field_with_meta(title='RT Dose datetime', description='Dato og tid for dosevolum', dicom="(300A, 0006)")
	plan_label_raw: Optional[str] = field_with_meta(title='Plan label raw', description='Plannavn (label) som angitt hos OIS', dicom="(300A, 0002)")
	plan_number: Optional[str] = field_with_meta(title='Plan number', description='Plannummer, NN eller NN.M, som tolket fra OIS. Angir behandlingsserie.replan', dicom="(300A, 0002)") # parsed from plan raw label, can be 0x so str
	plan_name: Optional[str] = field_with_meta(title='Plan name', description='Plannavn uten plannummer', dicom="(300A, 0002)")  # parsed from plan label
	total_dose_planned: Optional[float] = field_with_meta(title='Total dose planned [Gy]', description='Planlagt dose i denne behandlingsplanen. Hentet fra RT Plan', unit="Gy", dicom="(300A, 0026)")
	total_dose_delivered: Optional[float] = field_with_meta(title='Total dose delivered [Gy]', description='Levert dose i denne behandlingsplanen. Beregnet som summert dose til (primært) normeringsvolum i hver behandlingsfraksjon / RT Record', unit="Gy")
	fx_dose_planned: Optional[float] = field_with_meta(title='Fraction dose planned [Gy]', description='Planlagt fraksjonsdose. Planlagte dose / antall fraksjoner', unit="Gy", dicom="(300A, 0026) / (300a, 0078)")
	fxs_planned: Optional[int] = field_with_meta(title='Number of fractions planned', description='Planlagt antall fraksjoner', dicom="(300a, 0078)")
	fxs_delivered: Optional[int] = field_with_meta(title='Number of fractions delivered', description='Levert antall fraksjoner (fra tilhørende identifiserte behandlingsfraksjoner)', dicom="(3008,0022)")
	fx_delivered_from: Optional[int] = field_with_meta(title='Fraction number delivered from', description='Minste fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging', dicom="(3008,0022)")
	fx_delivered_to: Optional[int] = field_with_meta(title='Fraction number delivered to', description='Største fraksjonsnummer funnet i denne behandlingsplanen. Relevant for replanlegging', dicom="(3008,0022)")
	fx_delivered_from_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime delivered from', description='Første fraksjonsdato funnet i denne behandlingsplanen', dicom="(3008,0250)")
	fx_delivered_to_datetime: Optional[datetime] = field_with_meta(title='Fraction datetime delivered to', description='Siste fraksjonsdato funnet i denne behandlingsplanen', dicom="(3008,0250)")
	plan_completion: Optional[float] = field_with_meta(title='Plan completion', 
		description="Hvor mye av dose til normeringsvolum er levert i henhold til planlagt for hele behandlingsplanen. "
			" Den er beregnet som levert dose til primært normeringsvolum fra RT Records / planlagt dose til primært normeringsvolum "
			"Angis som tall mellom 0 (ingenting levert) og 1 (levert som planlagt)")
	beam_count: Optional[int] = field_with_meta(title='Beam count', description='Antall behandlingsfelt i denne behandlingsplanen', dicom="(300A,0080)")
	patient_orientation: Optional[Literal[patient_orientations_tuple]] = field_with_meta(title='Patient orientation', description='Pasientens leie', dicom="(0018, 5100)", values=patient_orientations_descr)
	tps_manufacturer: Optional[str] = field_with_meta(title='TPS manufacturer', description='Leverandør av programvare for behandlingsplan (TPS, Treatment Planning System)', dicom="(0008, 0070)")
	tps_software_name: Optional[str] = field_with_meta(title='TPS software name', description='Navn på programvare for behandlingsplan (TPS, Treatment Planning System)', dicom="(0008, 1090)")
	tps_software_version: Optional[str] = field_with_meta(title='TPS software version', description='Versjon av programvare for behandlingsplan (TPS, Treatment Planning System). Kommaseparert liste dersom det finnes flere.', dicom="(0018, 1020)")
	tx_modality: Optional[str] = field_with_meta(title='Treatment modality', description='Behandlingsmodalitet, basert på ``RadiationType``, inkluderer 3D eller ARC.', dicom="(300A, 00C6)")
	tx_time: Optional[float] = field_with_meta(title='Treatment time', description='Behandlingstid, kun relevant for brakyterapi', unit="s", dicom="(300A, 0286)")
	total_mu: Optional[float] = field_with_meta(title='Total MUs', description='Totalt antall Monitor Units (MUs) for hele behandlingsplanen', dicom="(300a, 0086)")
	dose_grid_res_x: Optional[float] = field_with_meta(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i X-retning', unit="mm", dicom="(0028, 0030)")
	dose_grid_res_y: Optional[float] = field_with_meta(title='Dose grid resolution X [mm]', description='Oppløsning i dosegrid i Y-retning', unit="mm", dicom="(0028, 0030)")
	heterogeneity_correction: Optional[str] = field_with_meta(title='Heterogeneity correction', description='Heterogeneitetskorreksjon for vev for doseberegning. Kommaseparert liste over ulike valg som er gjort.', dicom="(3004, 0014)", values=["IMAGE", "ROI_OVERRIDE", "WATER"])
	complexity: Optional[float] = field_with_meta(title='Plan complexity', description='Young\'s plankompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1). MU-vektet sum av hver beams kompleksitet, som igjen er en MU-vektet sum av kontrollpunktenes kompleksitet.')
	

class DVH(BaseModel):
	"""Målvolum og behandlingsvolum
	   ============================

	   Geometriske og dosimetriske data fra målvolum og behandlingsvolum"""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "structure"
	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')

	struct_course_id: Optional[str] = field_with_meta(title='FK Structure - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	struct_plan_uid: Optional[str] = field_with_meta(title='FK Structure - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')
	struct_uid: Optional[str] = field_with_meta(title='RT Structure SOP Instance UID', description='Denne RT Structure filens SOP Instance UID, brukes for å koble mot denne')
	ct_series_uid: Optional[str] = field_with_meta(title='CT Series UID', description='Koblingsnøkkel mot DICOM-datasett på Plan CT Series UID-nivå')

	is_dvh_plan_sum: Optional[bool] = field_with_meta(title='Is the DVH a plan-sum?', 
		description="Beskriver underliggende struktur en enkelt plan eller hele " 
			"behandlingsforløpet (for enkelt målvolum). Spesielt aktuell ved replan og plan-of-the-day. "
			"Aktuelle koblinger kan være Frame of Reference eller nummerering av plannavn, ikke ferdig implementert.")
	mapped_roi_name: Optional[str] = field_with_meta(title='Mapped ROI name', 
		description="Standardisert / mappet navn på struktur. Her kommer nok litt endringer, f.eks. egne variabler for union, "
			"doseregioner, høyre/venstre etc. Behov for egen parsing per institusjon, men håper vi kan ligge tett opp mot KREMT-standarden")

	roi_name: Optional[str] = field_with_meta(title='ROI name', description='Navn på struktur som angitt i TPS', dicom="(3006, 0026)")
	roi_type: Optional[Literal[roi_types]] = field_with_meta(title='ROI type', description='Strukturtype. Kun et fåtall av disse typene lagres, da kontrollstrukturer o.l. er uinteressant for registeret', dicom="(3006, 00A4)", values=roi_types)
	origin: Optional[str] = field_with_meta(title='Structure origin', description='Er strukturen inntegnet manuelt eller via AI-metoder? Kan hentes fra RT Struct tag, men må samle inn litt data før vi kan konkludere hva som kan brukes.')
	origin_software: Optional[str] = field_with_meta(title='Structure delineation software', description='Programvare benyttet for automatisk inntegning. Kan hentes fra RT Struct tag, men må samle inn litt data før vi kan konkludere hva som kan brukes.')
	volume: Optional[float] = field_with_meta(title='Structure volume [cc]', description='Strukturvolum som beregnet fra struktursettet', unit="cm3")
	min_dose: Optional[float] = field_with_meta(title='Voxelwise min dose [Gy]', description='Minste dose som beregnet fra struktursettet og RT dose', unit="Gy")
	mean_dose: Optional[float] = field_with_meta(title='Voxelwise mean dose [Gy]', description='Gjennomsnittlig dose som beregnet fra struktursettet og RT dose', unit="Gy")
	max_dose: Optional[float] = field_with_meta(title='Voxelwise max dose [Gy]', description='Største dose som beregnet fra struktursettet og RT dose', unit="Gy")
	dvh_string: Optional[str] = field_with_meta(title='DVH string [compressed]', 
		description=\
		"""Hele DVH-strengen for strukturen, som beregnet fra struktursettet og RT dose. Teknisk: Lagret som en b64-kodet gzippet streng av bitpakkede uint16, hvor 10 000 angir 100 % volum, med statiske 0.1 Gy bins.
		Ved datautlevering kan DVH-data eksporteres på ønsket format: CSV, Excel, JSON, PNG etc.
		Se f.eks. det relaterte prosjektet `DVH Toolkit <https://github.com/BergenParticleTherapy/DVHToolkit>`_ for tips til hvordan data kan behandles og NTCP-modelleres.
		Her følger et kodeeksempel i Python på hvordan dataene pakkes opp og ned fra en liste::
		
			def compress_bitpacking_b64_uint16(float_list):
				int_list = [int(x*100+0.5) for x in float_list]
				binary_data = struct.pack('>' + 'H' * len(int_list), *int_list)
				compressed_data = gzip.compress(binary_data)
				return base64.b64encode(compressed_data, pad=True).decode('ascii'))
			
			def decompress_bitpacking_b64_uint16(encoded_data):
				compressed_data = base64.b64decode(encoded_data)
				binary_data = gzip.decompress(compressed_data)
				int_list = struct.unpack(f'>{len(binary_data) // 2}H', binary_data)
				return [x/100 for x in int_list]
				
		""")
	# roi_coord_string: Optional[str] = field_with_meta(title='ROI string [compressed]', description='Hele ROI-strengen for strukturen, sikkert noe komprimert. Ikke i bruk')
	dist_to_ptv_min: Optional[float] = field_with_meta(title='Min distance to PTV [cm]', description='Minste avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	dist_to_ptv_mean: Optional[float] = field_with_meta(title='Mean distance to PTV [cm]', description='Gjennomsnittlig avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	dist_to_ptv_median: Optional[float] = field_with_meta(title='Median distance to PTV [cm]', description='Median avstand avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	dist_to_ptv_max: Optional[float] = field_with_meta(title='Max distance to PTV [cm]', description='Største avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	dist_to_ptv_25: Optional[float] = field_with_meta(title='25th percentile distance to PTV [cm]', description='25. persentil for avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	dist_to_ptv_75: Optional[float] = field_with_meta(title='75th percentile distance to PTV [cm]', description='75. persentil fo avstand mellom konturene for aktuell struktur og (union) PTV', unit="cm")
	scaling_factor: Optional[float] = field_with_meta(title='Dose scaling factor', 
		description="Skaleringsfaktor for levert DVH-dose. Alle DVH-er og doseverdier tilknyttet denne behandlingsplanen er skalert med denne faktoren."
					"Så dersom planlagt dose er 10 Gy, men bare 5 Gy er levert, vil denne faktoren være 0.5 og dose/volum-verdiene vil reflektere dette."
					"Den er beregnet som levert dose til primært normeringsvolum / planlagt dose til primært normeringsvolum")
	surface_area: Optional[float] = field_with_meta(title='ROI surface area [cm2]', description='Overflatearealet til strukturen', unit='cm2')
	ptv_overlap: Optional[float] = field_with_meta(title='PTV overlap [cm3]', description='Volum for overlapp mellom aktuell struktur og (union) PTV', unit="cm3")
	centroid: Optional[str] = field_with_meta(title='ROI centroid [cm,cm,cm]', description='Sentroiden til aktuell struktur', unit="[cm,cm,cm]")
	dist_to_ptv_centroids: Optional[float] = field_with_meta(title='Distance to PTV centroid [cm]', description='Avstand mellom sentroider for aktuell struktur og (union) PTV. Beregnet med ``shapely``', unit="cm")
	spread_x: Optional[float] = field_with_meta(title='Spread in X [cm]', description='Størrese i X-retning på rektangulær prisme som dekker aktuell struktur. Beregnet med ``shapely``', unit="cm")
	spread_y: Optional[float] = field_with_meta(title='Spread in Y [cm]', description='Størrese i Y-retning på rektangulær prisme som dekker aktuell struktur. Beregnet med ``shapely``', unit="cm")
	spread_z: Optional[float] = field_with_meta(title='Spread in Z [cm]', description='Størrese i Z-retning på rektangulær prisme som dekker aktuell struktur. Beregnet med ``shapely``', unit="cm")
	cross_section_max: Optional[float] = field_with_meta(title='Max cross section [cm2]', description='Største tverrsnitt for aktuell struktur over alle snitt. Beregnet med ``shapely``', unit="cm2")
	cross_section_median: Optional[float] = field_with_meta(title='Median cross section [cm2]', description='Median tverrsnitt for aktuell struktur over alle snitt. Beregnet med ``shapely``', unit="cm2")
	centroid_dist_to_iso_min: Optional[float] = field_with_meta(title='Centroid distance to isocenter min [cm]', description='Minste avstand mellom sentroide for aktuell struktur og isosenter (over alle felt). Beregnet med ``shapely``', unit="cm")
	centroid_dist_to_iso_max: Optional[float] = field_with_meta(title='Centroid distance to isocenter max [cm]', description='Største avstand mellom sentroide for aktuell struktur og isosenter (over alle felt). Beregnet med ``shapely``', unit="cm")
	integral_dose: Optional[float] = field_with_meta(title='Integral dose [cm3 Gy]', description='Integraldose til aktuell struktur, beregnet som gjennomsnittsdose * volum', unit="Gy cm3")
	color: Optional[str] = field_with_meta(title='ROI color', description='Farge til ROI som angitt i TPS.', dicom="(3006,002A)", unit="hex (RR,GG,BB)")
	D2: Optional[float] = field_with_meta(title='D2 [Gy]', description='Dose til 2% av aktuell struktur', unit="Gy")
	D10: Optional[float] = field_with_meta(title='D10% [Gy]', description='Dose til 10% av aktuell struktur', unit="Gy")
	D20: Optional[float] = field_with_meta(title='D20% [Gy]', description='Dose til 20% av aktuell struktur', unit="Gy")
	D30: Optional[float] = field_with_meta(title='D30% [Gy]', description='Dose til 30% av aktuell struktur', unit="Gy")
	D40: Optional[float] = field_with_meta(title='D40% [Gy]', description='Dose til 40% av aktuell struktur', unit="Gy")
	D50: Optional[float] = field_with_meta(title='D50% [Gy]', description='Dose til 50% av aktuell struktur', unit="Gy")
	D60: Optional[float] = field_with_meta(title='D60% [Gy]', description='Dose til 60% av aktuell struktur', unit="Gy")
	D70: Optional[float] = field_with_meta(title='D70% [Gy]', description='Dose til 70% av aktuell struktur', unit="Gy")
	D80: Optional[float] = field_with_meta(title='D80% [Gy]', description='Dose til 80% av aktuell struktur', unit="Gy")
	D90: Optional[float] = field_with_meta(title='D90% [Gy]', description='Dose til 90% av aktuell struktur', unit="Gy")
	D98: Optional[float] = field_with_meta(title='D98% [Gy]', description='Dose til 98% av aktuell struktur ', unit="Gy")
	D2cc: Optional[float] = field_with_meta(title='D2cc [Gy]', description='Dose til 2cc av aktuell struktur', unit="Gy")
	V5Gy: Optional[float] = field_with_meta(title='V5Gy [%]', description='Volumet av aktuell struktur som mottar 5 Gy', unit="%")
	V10Gy: Optional[float] = field_with_meta(title='V10Gy [%]', description='Volumet av aktuell struktur som mottar 10 Gy', unit="%")
	V15Gy: Optional[float] = field_with_meta(title='V15Gy [%]', description='Volumet av aktuell struktur som mottar 15 Gy', unit="%")
	V20Gy: Optional[float] = field_with_meta(title='V20Gy [%]', description='Volumet av aktuell struktur som mottar 20 Gy', unit="%")
	V25Gy: Optional[float] = field_with_meta(title='V25Gy [%]', description='Volumet av aktuell struktur som mottar 25 Gy', unit="%")
	V30Gy: Optional[float] = field_with_meta(title='V30Gy [%]', description='Volumet av aktuell struktur som mottar 30 Gy', unit="%")
	V35Gy: Optional[float] = field_with_meta(title='V35Gy [%]', description='Volumet av aktuell struktur som mottar 35 Gy', unit="%")
	V40Gy: Optional[float] = field_with_meta(title='V40Gy [%]', description='Volumet av aktuell struktur som mottar 40 Gy', unit="%")
	V45Gy: Optional[float] = field_with_meta(title='V45Gy [%]', description='Volumet av aktuell struktur som mottar 45 Gy', unit="%")
	V50Gy: Optional[float] = field_with_meta(title='V50Gy [%]', description='Volumet av aktuell struktur som mottar 50 Gy', unit="%")
	V55Gy: Optional[float] = field_with_meta(title='V55Gy [%]', description='Volumet av aktuell struktur som mottar 55 Gy', unit="%")
	V60Gy: Optional[float] = field_with_meta(title='V60Gy [%]', description='Volumet av aktuell struktur som mottar 60 Gy', unit="%")
	V65Gy: Optional[float] = field_with_meta(title='V65Gy [%]', description='Volumet av aktuell struktur som mottar 65 Gy', unit="%")
	V70Gy: Optional[float] = field_with_meta(title='V70Gy [%]', description='Volumet av aktuell struktur som mottar 70 Gy', unit="%")
	V95: Optional[float] = field_with_meta(title='V95% [%]', description='Volumet av aktuell struktur som mottar 95% av planlagt dose til målvolum', unit="%")

class DR(BaseModel):
	"""Oversikt over normeringsvolum:
	   ==============================
	
		Oversikt over normeringsvolum, både det primære som brukes som mål på fraksjonsdose og støtte-normeringsvolum
	
	"""

	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "dosereference"

	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')
	dr_course_id: Optional[str] = field_with_meta(title='FK Dose Reference - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	dr_plan_uid: Optional[str] = field_with_meta(title='FK Dose Reference - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	ref_dr_name: Optional[str] = field_with_meta(title='Referenced Dose Reference name', description='Navn på normeringsvolum, fra Description taggen', dicom="(300A,0016)")
	dr_type: Optional[Literal["POINT", "VOLUME", "COORDINATES", "SITE"]] = \
		 field_with_meta(title='Dose Reference structure type', description='Strukturtype på normeringsvolum', values=["POINT", "VOLUME", "COORDINATES", "SITE"], dicom="(300A,0014)")
	dr_ref_type: Optional[Literal["TARGET", "ORGAN_AT_RISK"]] = \
		field_with_meta(title='Dose Reference type', description='Kategori av normeringsvolum', dicom="(300A,0020)", values=["TARGET", "ORGAN_AT_RISK"])
	dr_dose_planned: Optional[float] = field_with_meta(title='Planned dose to Dose Reference [Gy]', description='Planlagt dose til normeringsvolum', unit="Gy", dicom="(300A,0026)")
	dr_dose_delivered: Optional[float] = field_with_meta(title='Delivered dose to Dose Reference [Gy]', description='Levert dose til normeringsvolum, som summert fra behandlingsfraksjonene', unit="Gy")
	dr_max_dose: Optional[float] = field_with_meta(title='Max dose to Dose Reference [Gy]', description='Største tillatt dose til normeringsvolum', unit="Gy")
	dr_is_primary: Optional[bool] = field_with_meta(title='Is the Dose Reference primary', description="Er det primært normeringsvolum? -> Brukes til beregning av leverte doser", dicom="(300A,061B)")

class Beam(BaseModel):
	"""Oversikt over behandlingsfelt
	   =============================
	
	"""
	# redcap_repeat_instance: str = 'new'
	# redcap_repeat_instrument: str = "beam"

	record_id: Optional[str] = field_with_meta(title='Koblingsnøkkel i NORPREG', description='Angis automatisk for hver pasient. Foreslått format er 7-karakter heksadesimal (f.eks. a72bf40)')
	beam_course_id: Optional[str] = field_with_meta(title='FK Beam - Course ID', description='Koblingsnøkkel mot Course ID på OIS-nivå')
	beam_plan_uid: Optional[str] = field_with_meta(title='FK Beam - Plan UID', description='Koblingsnøkkel mot DICOM-datasett på Plan UID-nivå')

	beam_tx_modality: Optional[str] = field_with_meta(title='Treatment modality', 
		description='Behandlingsmodalitet tolket fra ``radiation_type``: Får 3D / arc modifikator dersom det er benyttet.', dicom = "(300A,00C6)")

	beam_number: Optional[int] = field_with_meta(title='Beam number', description='Tallangivelsen for dette feltet', dicom='(300A, 00C0)')
	beam_name: Optional[str] = field_with_meta(title='Beam name', description='Feltnavn, inneholder ofte vinkelinformasjon', dicom='(300A, 00C3) / (300A, 00C2)')
	fx_grp_number: Optional[int] = field_with_meta(title='Fraction group number', description='Gruppenummeret til fraksjonen', dicom='(300A, 0071)')
	fx_count: Optional[int] = field_with_meta(title='Fraction count', description='Totalt antall fraksjoner for dette feltet', dicom='(300A, 0078)')
	fx_grp_beam_count: Optional[int] = field_with_meta(title='Fraction group beam count', description='Antall felt i denne fraksjonsgruppen')
	beam_dose: Optional[float] = field_with_meta(title='Beam dose [Gy]', description='Planlagt dose for dette feltet', unit="Gy", dicom='(300A, 008B)')
	beam_mu: Optional[float] = field_with_meta(title='Beam Monitor Units', description='Antall Monitor Units (MUs) for dette feltet')
	radiation_type: Optional[Literal["PHOTON", "ELECTRON", "NEUTRON", "PROTON"]] =  field_with_meta(
			title='Radiation type', 
			description='Strålingstype for dette feltet (uten 3D modifikator)', 
			dicom='(300A, 00C6)',
			values = ["PHOTON", "ELECTRON", "NEUTRON", "PROTON"]
	)
	beam_energy_min: Optional[float] = field_with_meta(title='Min beam energy [MV / MeV]', description='Minste energi for strålefeltet. Enheten avhenger av strålingstypen', unit="MV / MeV", dicom='(300A, 0114)')
	beam_energy_max: Optional[float] = field_with_meta(title='Max beam energy [MV / MeV]', description='Største energi for strålefeltet. Enheten avhenger av strålingstypen', unit="MV / MeV", dicom='(300A, 0114)')
	beam_type: Literal["STATIC", "DYNAMIC"] = field_with_meta(title='Beam type', description='Felttype', dicom='(300A,00C4)')
	control_point_count: Optional[int] = field_with_meta(title='Control point count', description='Antall kontrollpunkter for dette feltet')
	gantry_start: Optional[float] = field_with_meta(title='Gantry start [deg]', description='Gantry startvinkel', unit="deg", dicom='(300A, 011E)')
	gantry_end: Optional[float] = field_with_meta(title='Gantry end [deg]', description='Gantry sluttvinkel', unit="deg", dicom='(300A, 011E)')
	gantry_rot_dir: Literal["CW", "CC", "NONE"] = field_with_meta(title='Gantry rotation direction', description='Retning til gantryrotasjon', values=["CW", "CC", "NONE"], dicom='(300A, 011F)')
	gantry_range: Optional[float] = field_with_meta(title='Gantry range [deg]', description='Hvor mye gantry roterer', unit="deg", dicom='(300A, 011E)')
	gantry_min: Optional[float] = field_with_meta(title='Gantry min [deg]', description='Minste gantryvinkel', unit="deg", dicom='(300A, 011E)')
	gantry_max: Optional[float] = field_with_meta(title='Gantry max [deg]', description='Største gantryvinkel', unit="deg", dicom='(300A, 011E)')
	collimator_start: Optional[float] = field_with_meta(title='Collimator start [deg]', description='Kollimator startvinkel', unit="deg", dicom='(300A, 0120)')
	collimator_end: Optional[float] = field_with_meta(title='Colimator end [deg]', description='Kollimator sluttvinkel', unit="deg", dicom='(300A, 0120)')
	collimator_rot_dir: Literal["CW", "CC", "NONE"] = field_with_meta(title='Collimator rotation direction', description='Retning til kollimatorrotasjon', values=["CW", "CC", "NONE"], dicom='(300A, 0121)')
	collimator_range: Optional[float] = field_with_meta(title='Collimator range [deg]', description='Hvor mange grader kollimator roterer', dicom='(300A, 0120)')
	collimator_min: Optional[float] = field_with_meta(title='Collimator min [deg]', description='Minste kollimatorvinkel', unit="deg", dicom='(300A, 0120)')
	collimator_max: Optional[float] = field_with_meta(title='Collimator max [deg]', description='Største kollimatorvinkel', unit="deg", dicom='(300A, 0120)')
	couch_start: Optional[float] = field_with_meta(title='Couch start [deg]', description='Bord startvinkel', unit="deg", dicom='(300A, 0122)')
	couch_end: Optional[float] = field_with_meta(title='Cough end [deg]', description='Bord sluttvinkel', unit="deg", dicom='(300A, 0122)')
	couch_rot_dir: Literal["CW", "CC", "NONE"] = field_with_meta(title='Cough rotation direction', description='Retning til bordrotasjon', values=["CW", "CC", "NONE"], dicom='(300A, 0122)')
	couch_range: Optional[float] = field_with_meta(title='Cough range [deg]', description='Hvor mange grader bord roterer', dicom='(300A, 0122)')
	couch_min: Optional[float] = field_with_meta(title='Cough min [deg]', description='Største bordvinkel', unit="deg", dicom='(300A, 0122)')
	couch_max: Optional[float] = field_with_meta(title='Cough max [deg]', description='Minste bordvinkel', unit="deg", dicom='(300A, 0122)')
	beam_dose_pt: Optional[str] = field_with_meta(title='Beam dose Specification point [Gy]', description='Dose til primært normeringsvolum for dette feltet', unit='Gy', dicom='(300A, 0082)')
	isocenter: Optional[str] = field_with_meta(title='Isocenter position', description='Isosenterposisjon i x,y,z', unit="[cm, cm, cm]", dicom='(300A, 012C)')
	ssd: Optional[float] = field_with_meta(title='Source to surface distance', description='Avstand mellom kilde og overflate. Dersom behandlingsmodalitetet er ARC, beregnes gjennomsnittet.', unit="cm", dicom='(300A, 0130)')
	treatment_machine: Optional[str] = field_with_meta(title='Treatment machine name', description='(Lokalt) navn på behandlingsapparat', dicom='(300A, 00B2)')
	
	scan_mode: Literal["NONE", "UNIFORM", "MODULATED", "MODULATED_SPEC"] = \
		field_with_meta(title='Scan mode', description='Hvordan strålen scannes under behandling.', values=["NONE", "UNIFORM", "MODULATED", "MODULATED_SPEC"], dicom="(300A, 0308)")

	scan_spot_count: Optional[int] = field_with_meta(title='Scan spot count', description='Hvor mange punkter som benyttes under spot scanning', dicom="(300A, 0392)")
	beam_mu_per_deg: Optional[float] = field_with_meta(title='Beam MUs per degree', description='Hvor mange monitoreringsenheter per rotasjonsgrad')
	beam_mu_per_cp: Optional[float] = field_with_meta(title='Beam MUs per control point', description='Hvor mange monitoreringsenheter per kontrollpunkt')
	area_min: Optional[float] = field_with_meta(title='Area min [cm2]', description='Minste feltareal', unit='cm2')
	area_mean: Optional[float] = field_with_meta(title='Area mean [cm2]', description='Gjennomsnittlig feltareal', unit='cm2')
	area_median: Optional[float] = field_with_meta(title='Area median [cm2]', description='Median feltareal', unit='cm2')
	area_max: Optional[float] = field_with_meta(title='Area max [cm2]', description='Største feltareal', unit='cm2')
	perim_min: Optional[float] = field_with_meta(title='Beam perimeter min [cm]', description='Minste feltomkrets', unit='cm')
	perim_mean: Optional[float] = field_with_meta(title='Beam perimeter mean [cm]', description='Gjennomsnittlig feltomkrets', unit='cm')
	perim_median: Optional[float] = field_with_meta(title='Beam perimeter median [cm]', description='Median feltomkrets', unit='cm')
	perim_max: Optional[float] = field_with_meta(title='Beam perimeter max [cm]', description='Største feltomkrets', unit='cm')
	x_perim_min: Optional[float] = field_with_meta(title='Beam perimeter X min [cm]', description='Minste feltomkrets (X)', unit='cm')
	x_perim_mean: Optional[float] = field_with_meta(title='Beam perimeter X mean [cm]', description='Gjennomsnittlig feltomkrets (X)', unit='cm')
	x_perim_median: Optional[float] = field_with_meta(title='Beam perimeter X median [cm]', description='Median feltomkrets (X)', unit='cm')
	x_perim_max: Optional[float] = field_with_meta(title='Beam perimeter X max [cm]', description='Største feltomkrets (X)', unit='cm')
	y_perim_min: Optional[float] = field_with_meta(title='Beam perimeter Y min [cm]', description='Minste feltomkrets (Y)', unit='cm')
	y_perim_mean: Optional[float] = field_with_meta(title='Beam perimeter Y mean [cm]', description='Gjennomsnittlig feltomkrets (Y)', unit='cm')
	y_perim_median: Optional[float] = field_with_meta(title='Beam perimeter Y median [cm]', description='Median feltomkrets (Y)', unit='cm')
	y_perim_max: Optional[float] = field_with_meta(title='Beam perimeter Y max [cm]', description='Største feltomkrets (Y)', unit='cm')
	complexity_min: Optional[float] = field_with_meta(title='Field complexity min', description='Minste Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_mean: Optional[float] = field_with_meta(title='Field complexity mean', description='Gjennomsnittlig Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_median: Optional[float] = field_with_meta(title='Field complexity median', description='Median Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	complexity_max: Optional[float] = field_with_meta(title='Field complexity max', description='Største Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1) over alle kontrollpunktene.')
	cp_mu_min: Optional[float] = field_with_meta(title='Control point MU min', description='Lavest MU over alle kontrollpunktene')
	cp_mu_mean: Optional[float] = field_with_meta(title='Control point MU mean', description='Gjennomsnittlig MU over alle kontrollpunktene')
	cp_mu_median: Optional[float] = field_with_meta(title='Control point MU median', description='Median MU over alle kontrollpunktene')
	cp_mu_max: Optional[float] = field_with_meta(title='Control point MU max', description='Største MU over alle kontrollpunktene')
	beam_complexity: Optional[float] = field_with_meta(title='Beam complexity', description='Young\'s feltkompleksitet, beregnet ved jevn vekting i X- og Y- planet (c1=c2=1). MU-vektet sum av kontrollpunktenes kompleksitet.')