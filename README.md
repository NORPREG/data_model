# Norsk proton- og stråleterapiregister – Datamodell

Datamodellen for **NORPREG** (Norsk proton- og stråleterapiregister. Denne definerer strukturen for innsamling, lagring og behandling av data fra stråleterapibehandlinger ved norske helseinstitusjoner.

## Om registeret

NORPREG er et nasjonalt kvalitetsregister som dokumenterer stråleterapibehandlinger med fokus på pasientsikkerhet, behandlingskvalitet og resultater. Registeret samler data fra flere kilder:

- **DICOM RT-objekter** – Behandlingsplaner og doseinformasjon fra terapimaskiner
- **Nasjonalt Pasientregister (NPR)** – Offisiell helsefaglig dokumentasjon
- **Elektronisk pasientjournal (EPJ)** – Kliniske data og behandlingshistorikk
- **Strukturdata** – Geometriske data, organkonturering og dose-volume histogramer

## Dokumentasjon

Den fullstendige dokumentasjonen av datamodellen er tilgjengelig på [Read the Docs](https://norpreg-data-model.readthedocs.io/).
Mer informasjon om registeret finnes også på https://norpreg.no.

Dokumentasjonen genereres automatisk fra Pydantic-datamodellene ved hjelp av `sphinx-pydantic`.

## Struktur

```
model/
├── Datamodel/
│   ├── RT.py          # Stråleterapi-behandlinger fra DICOM
│   ├── NPR.py         # Data fra Nasjonalt Pasientregister
│   ├── EPJ.py         # Data fra elektronisk pasientjournal
│   ├── Strukturer.py  # Geometriske data og strukturer
│   ├── Kodeliste.py   # Koblingsnøkler og krypteri
│   └── __init__.py
```

## Lisens

Se [LICENSE](LICENSE) for detaljer.