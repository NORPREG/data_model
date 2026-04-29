Datamodell for Norsk proton- og stråleterapiregister
====================================================

Datamodellen for Norsk proton- og stråleterapiregister (NORPREG) er strukturert rundt flere komplementære datakilder som til sammen gir en komplett oversikt over behandling, pasienter og planlegging.

Kilder i datamodellen
---------------------

**Stråleterapi (RT)** - Hovedkilden for behandlingsdata fra DICOM RT-objekter, inkludert doseplaner, fraksjoner og behandlingsparametere.

**Nasjonalt Pasientregister (NPR)** - Standardisert rapportering fra stråleterapienhetene, med opplysninger på fraksjonsnivå med enkel dose, omsorgsnivå, diagnose og behandlingsintensjon.

**Strukturer** - Geometriske data fra doseplaner, inkludert organkonturering (ROI), Dose-Volume Histogramer (DVH) og beregnet volumdata lagret i Parquet-format for effektiv lagring og analyse. Dette datalageret er ikke en del av det den sentrale registerdatabasen.

**Kliniske data** - Samlet pasient- og behandlingsinformasjon som kobles mot relevante kodeverk (ICD-10, SNOMED CT, AJCC, MedDRA/CTCAE osv.). Hentes fra EPJ via Strukturert Journal for Kreft.

**Kodelister** - Sentral lagring av krypterte personidentifiserbare opplysninger, koblingsnøkler og dataflyt med eksterne kilder.

Modell for stråleterapi
-----------------------

.. automodule:: Datamodel.RT
    :members:
    :undoc-members:

Modell for Nasjonalt Pasientregister-data
-------------------------------------

Denne modulen inneholder data fra NPR og representerer offisiell helsefaglig dokumentasjon fra sykehusene. Den inkluderer opplysninger om inn- og utdatoer, omsorgsnivå, prosedyrekoder, diagnose, behandlingsintensjon og maskin-ID.

.. automodule:: Datamodel.NPR
    :members:
    :undoc-members:

Modell for strukturer
---------------------

Denne modulen lagrer geometriske data fra doseplaner, inkludert organkonturering (ROI-koordinater), Dose-Volume Histogramer (DVH) og beregnet volumdata. Dataene lagres effektivt i Parquet-format og er organisert per behandlingsplan med tilknyttet metadata om helseforetak, plan-år og pseudonymisert koblingsnøkkel.

.. automodule:: Datamodel.Strukturer
    :members:
    :undoc-members:

Modell for kliniske data
------------------------
Det foreligger mange parametere som er koblet mot ulike kodeverk som ICD10, SNOMED CT, AJCC, MedDRA CTCAE o.l., det vil fremgå hvor der et aktuelt.
Denne modulen er under arbeid, og reflekterer "Innrapportering til NORPREG v1" eksportskjema fra DIPS.

.. automodule:: Datamodel.EPJ
    :members:
    :undoc-members:

Modell for kodeliste for koblingsnøkler
---------------------------------------
Denne modellen benyttes for å lagre og kryptere direkte personidentifiserbare opplysninger i registeret, samt holde rede på dataflyt med eksterne kilder
og loggføre reservasjonsstatus. Deler av denne kodelisten er kryptert.

.. automodule:: Datamodel.Kodeliste
    :members:
    :undoc-members: