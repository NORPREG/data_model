NORPREG Datamodell
==================

Velkommen til dokumentasjonen for **Norsk proton- og stråleterapiregister (NORPREG)** – et nasjonalt kvalitetsregister for stråleterapibehandlinger.

Datamodellen beskriver strukturen for innsamling, lagring og behandling av data fra stråleterapienheter ved norske helseinstitusjoner.

Introduksjon
============

NORPREG er et nasjonalt register som dokumenterer stråleterapibehandlinger med fokus på pasientsikkerhet, behandlingskvalitet og resultater. Registeret samler data fra flere kilder og lagrer dem i en strukturert datamodell basert på Pydantic.

Datamodellen inkluderer:

- **Stråleterapi (RT)** – Behandlingsplaner og doseinformasjon fra fagsystemer for stråleterapi (TPS/OIS)
- **Nasjonalt Pasientregister (NPR)** – Offisiell helsefaglig dokumentasjon
- **Kliniske data (EPJ)** – Data fra elektronisk pasientjournal
- **Strukturer** – Geometriske data, organkonturering og dose-volume histogrammer
- **Kodelister** – Kryptert lagring av personidentifiserbare opplysninger

.. toctree::
   :maxdepth: 1
   :caption: Dokumentasjon

   models