from typing_extensions import Annotated

from pydantic import BaseModel, PlainSerializer, BeforeValidator, Field
from typing import Optional, List, Literal
from datetime import datetime


def field_with_meta(title, description="", values=list(), dicom=None, unit=None, terminology=None, encrypted=False, default=None, default_factory=None):
	values_str = len(values) and "**Mulige verdier:**\n\n" + "\n\n".join([f"* {k}" for k in values]) or ""
	unit_str = unit and f"**Enhet**: {unit}\n\n" or ""
	unit_str = unit_str.replace("cm2", "cm\ :sup:`2`")
	unit_str = unit_str.replace("cm3", "cm\ :sup:`3`")
	terminology_str = terminology and f"**Kodeverk:** {terminology}" or ""
	dicom_str = dicom and f"\n\n**DICOM**: ``{dicom}``" or ""
	encrypted_str = encrypted and "**Kryptert datafelt**\n\n" or ""
	title_str = len(title) and f"**{title}**" or ""
	if len(description):
		description_added = f"{title_str}: {description}\n\n" + unit_str + values_str + dicom_str + encrypted_str
	else:
		description_added = f"{title_str}\n\n" + unit_str + values_str + dicom_str + encrypted_str


	if not default_factory:
		return Field(default=default, alias=title, description=description_added)
	else:
		return Field(default_factory=default_factory, alias=title, description=description_added)