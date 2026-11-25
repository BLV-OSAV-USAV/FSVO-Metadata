🚧 **Dieses Projekt befindet sich in aktiver Entwicklung.**

⚠️ **Alle Daten sind frei gewählt und dienen ausschliesslich Testzwecken.**

[![Datensätze zusammenführen](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/combine-datasets.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/combine-datasets.yml)
[![I14Y-Datensätze ABN](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_abn.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_abn.yml)
[![I14Y-Datensätze PROD](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_prod.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_prod.yml)
[![I14Y-Behördenleistungen ABN](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_abn.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_abn.yml)
[![I14Y-Behördenleistungen PROD](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_prod.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_prod.yml)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Lizenz CC BY-ND 4.0](https://img.shields.io/badge/License-CC%20BY--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nd/4.0/)
[![Letzter GitHub-Commit](https://img.shields.io/github/last-commit/BLV-OSAV-USAV/FSVO-Metadata.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/commits)
[![GitHub-Issues](https://img.shields.io/github/issues/BLV-OSAV-USAV/FSVO-Metadata.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/issues)

Dieses Repository enthält Metadaten zu Datensätzen und Behördenleistungen des Bundesamts für Lebensmittelsicherheit und Veterinärwesen (BLV). Python-Skripte führen die Metadaten zusammen und prüfen sie anhand von JSON-Schemas. Die zusammengeführten Metadaten stehen unter `data/processed` für den Datenkatalog des Bundesamts für Landwirtschaft (BLW) bereit. Die Metadaten sind mit I14Y und opendata.swiss kompatibel. [I14Y](https://www.i14y.admin.ch/) · [opendata.swiss](https://opendata.swiss) · [Webanwendung des BLW-Datenkatalogs](https://github.com/blw-ofag-ufag/data-catalog)

## Metadaten an I14Y übermitteln

Die Harvester im Ordner `i14y/` übermitteln Metadaten zu Datensätzen und Behördenleistungen an die I14Y-Partner-API. Für beide Arten von Metadaten gibt es je einen GitHub-Actions-Workflow für die Abnahmeumgebung (ABN) und die Produktionsumgebung (PROD). [Harvester-Code](i14y/)

- **Datensätze** stammen aus `data/processed/datasets.json`. Der Workflow **Combine Datasets** erzeugt diese Datei. Trage in der Konfiguration unter `I14Y_DATASET_IDENTIFIERS` die gewünschten `dct:identifier` ein. Eine leere Auswahl übermittelt keine Datensätze. [Datensatzquelle](data/processed/datasets.json) · [Konfiguration](i14y/config.py)
- **Behördenleistungen** stammen aus `data/publicservices/publicservices.json`. Verwende die Beispiel-JSON als Vorlage und halte die erste Kennung jeder Leistung stabil. Anhand dieser Kennung findet und aktualisiert der Harvester bestehende Einträge. [JSON-Quelle](data/publicservices/publicservices.json) · [Beispiel-JSON](data/publicservices/publicservices.example.json) · [Erfassungsanleitung](data/publicservices/README.md)

Die Vorlage verwendet das I14Y-Schreibformat. Codelistenwerte haben die Form `{"code": "de"}`. Herausgeber und Kanalbetreiber werden als Organisationskennungen wie `{"identifier": "CH_BLV"}` erfasst. Für `isDescribedAt`, `relations` und `requires` verwendest du `{"id": "<I14Y-UUID>"}` mit der UUID eines bestehenden I14Y-Eintrags. Ersetze die Beispiel-URL, E-Mail-Adressen und Codes durch passende Werte. Optionale Felder kannst du weglassen, wenn sie für die Leistung keine Rolle spielen. [Schreibschema der I14Y-Partner-API](https://apiconsole.i14y.admin.ch/partner/v1/Release.json)

Führe im Stammverzeichnis des Repositorys `python -m i14y.publicservices.harvester` aus, um die JSON-Struktur und die Pflichtangaben der Behördenleistungen lokal zu prüfen. Zum Schreiben an die API braucht der Harvester `--apply` und ein Zugriffstoken in `ACCESS_TOKEN`. Lokale Läufe verwenden standardmässig ABN. Mit `I14Y_ENVIRONMENT=PROD` wählst du die Produktionsumgebung.

### GitHub Actions und Laufprotokolle

Über **Run workflow** auf der jeweiligen Actions-Seite kannst du alle vier Harvester manuell starten. Der PROD-Workflow für Datensätze läuft zusätzlich montags um 03.00 Uhr UTC. Jeder Workflow bezieht die I14Y-Client-ID und das Client-Secret seiner Umgebung aus den GitHub-Actions-Secrets.

Die Workflows laden die Laufprotokolle als Artefakte hoch. Nach einem erfolgreichen Lauf auf einem Branch speichert der Workflow das aktuelle Protokoll auch unter `logs/i14y/<harvester>/<umgebung>/latest.txt` auf diesem Branch. Jeder erfolgreiche Lauf ersetzt die vorherige Fassung am selben Pfad. Ältere Fassungen sind im Git-Verlauf verfügbar.
