Modell for stråleterapi
-----------------------

.. automodule:: Datamodel.RT
    :members:

Modell for Nasjonalt Pasientregister-data
-------------------------------------

Denne modulen inneholder data fra NPR og representerer offisiell helsefaglig dokumentasjon fra sykehusene. Den inkluderer opplysninger om inn- og utdatoer, omsorgsnivå, prosedyrekoder, diagnose, behandlingsintensjon og maskin-ID.

.. automodule:: Datamodel.NPR
    :members:

Modell for strukturer
---------------------

Denne modulen lagrer geometriske data fra doseplaner, inkludert organkonturering (ROI-koordinater), Dose-Volume Histogramer (DVH) og beregnet volumdata. Dataene lagres effektivt i Parquet-format og er organisert per behandlingsplan med tilknyttet metadata om helseforetak, plan-år og pseudonymisert koblingsnøkkel.

.. automodule:: Datamodel.Strukturer
    :members:

Modell for kliniske data
------------------------
Det foreligger mange parametere som er koblet mot ulike kodeverk som ICD10, SNOMED CT, AJCC, MedDRA CTCAE o.l., det vil fremgå hvor der et aktuelt.
Denne modulen er under arbeid, og reflekterer "Innrapportering til NORPREG v1" eksportskjema fra DIPS.

.. automodule:: Datamodel.EPJ
    :members:

Modell for kodeliste for koblingsnøkler
---------------------------------------
Denne modellen benyttes for å lagre og kryptere direkte personidentifiserbare opplysninger i registeret, samt holde rede på dataflyt med eksterne kilder
og loggføre reservasjonsstatus. Deler av denne kodelisten er kryptert.

.. automodule:: Datamodel.Kodeliste
    :members:
