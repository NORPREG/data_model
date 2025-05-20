Datamodell for Norsk proton- og stråleterapiregister
====================================================

Modellen for stråleterapi er ganske moden, og brukes i produksjon nå.
Modellen for kliniske data er ikke ennå helt klar, men vil samkjøres med innmeldingsskjema fra DIPS når det går ut i 1.0.

Modell for stråleterapi
-----------------------
Det som ligger her er synkronisert mot datamodellen i REDCap.

.. automodule:: Datamodel.RT
    :members:

Modell for kliniske data
------------------------
Det foreligger mange parametere som er koblet mot ulike kodeverk som ICD10, SNOMED CT, AJCC, MedDRA CTCAE o.l., det vil fremgå hvor der et aktuelt.

.. automodule:: Datamodel.Clinical
    :members:

