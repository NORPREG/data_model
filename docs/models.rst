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

Modell for kodeliste for koblingsnøkler
---------------------------------------
Denne modellen benyttes for å lagre og kryptere direkte personidentifiserbare opplysninger i registeret, samt holde rede på dataflyt med eksterne kilder
og loggføre reservasjonsstatus.

Deler av denne kodelisten er kryptert. Da benyttes AES, CBC og PKCS#7. Nøkkelen er sikret i produksjonsmiljøet, mens IV er enkodet i tekstfeltet med `iv_b64:cipher_b64`.

.. automodule:: Datamodel.Kodeliste
    :members: