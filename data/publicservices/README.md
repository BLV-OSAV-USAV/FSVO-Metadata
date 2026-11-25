# Behördenleistungen für I14Y erfassen

Ergänze [`publicservices.json`](publicservices.json) um ein JSON-Objekt pro Behördenleistung. Die Datei enthält eine Liste. Verwende [`publicservices.example.json`](publicservices.example.json) als Vorlage und ersetze deren Beispielwerte. Der Harvester verpackt jeden Eintrag beim Senden als `{"data": {...}}`.

## Pflichtangaben

| Feld | Was wird erfasst? |
| --- | --- |
| `identifiers` | Eine Liste eindeutiger Kennungen, etwa `["FSVO_SERVICE_001"]`. Die erste Kennung dient dem Harvester zur Suche nach einem bestehenden Eintrag. Halte sie bei Aktualisierungen stabil. Verwende Buchstaben ohne Akzente, Ziffern, Bindestriche und Unterstriche. |
| `name` | Kurzer Name als Sprachobjekt, etwa `{"de": "Name der Leistung"}`. |
| `description` | Mehrsprachige Beschreibung der Leistung, ihrer Zielgruppe und ihres Nutzens. Mindestens eine Sprachversion ist erforderlich. Für Leistungen des Bundes empfiehlt I14Y Deutsch, Französisch und Italienisch für Name und Beschreibung. |
| `publisher` | Kennung der herausgebenden Organisation als Objekt, etwa `{"identifier": "CH_BLV"}`. |

Sprachobjekte unterstützen die Schlüssel `de`, `fr`, `it`, `en` und `rm`. Das Feld `languages` erfasst separat, in welchen Sprachen die Leistung selbst verfügbar ist. [I14Y-Handbuch zu den Eingabefeldern](https://handbook.i14y.admin.ch/de/anhang/eingabefelder/eingabefelder_behoerdenleistung/)

## Codelisten und Vokabulare

Übernimm den Wert aus der Spalte **Code** der jeweiligen Liste. Codelistenwerte werden als Objekte mit `code` erfasst, beispielsweise `"languages": [{"code": "de"}, {"code": "fr"}]`. Mehrere Codes kommen als separate Objekte in dieselbe Liste.

| JSON-Feld | Bedeutung und Quelle |
| --- | --- |
| `businessEvents` | Situationen von Unternehmen, etwa Import und Export (`BE-ImportExport`). [I14Y-Geschäftssituationen](https://www.i14y.admin.ch/de/catalog/concepts/08dc74b4-30d4-be8d-ba53-91a1201ac86b/description) |
| `lifeEvents` | Lebenslagen natürlicher Personen. Wenn keine passt, kann das Feld entfallen. [I14Y-Lebenslagen](https://www.i14y.admin.ch/de/catalog/concepts/08dc65d1-652a-3546-9100-faffbaf7c6fd/description) |
| `thematicAreas`, `sectors` | Themen und Sektoren, etwa Landwirtschaft (`109)). I14Y verwendet derzeit dieselbe Liste für beide Felder. [I14Y-Themenliste](https://www.i14y.admin.ch/de/concepts/08da58dc-4dc8-f9cb-b6f2-7d16b3fa0cde) |
| `languages` | Sprachen, in denen die Leistung angeboten wird. [ISO-639-Sprachcodes](https://www.loc.gov/standards/iso639-2/php/code_list.php) |
| `channels[].type` | Typ eines Zugangskanals als einzelnes Code-Objekt. Der exportierte Webkanal verwendet `{"code": "b37115f83e"}`. [EU-Vokabular für Kommunikationskanäle](https://data.europa.eu/snb/com-channel/) |
| `spatial` | Räumliche Abdeckung als Liste von Zeichenketten, etwa `["CH"]` für die Schweiz. [EU-Ländervokabular](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/authority/country) |
| `spatialCH` | Schweizer Gebietscodes als Liste von Code-Objekten. Falls die gültige I14Y-Kennung unklar ist, verwende für die Erfassung zunächst `spatial`. [I14Y-Handbuch zum Abruf von Codelisten](https://handbook.i14y.admin.ch/de/metadaten_abrufen/api/) |

## Zugangskanäle, Verweise und Kontakte

- `channels` beschreibt Zugangswege wie ein Online-Portal oder eine Kontaktstelle. Jeder Kanal braucht einen eigenen `identifier`. Je nach Kanal kannst du `type`, `url`, `email`, `phone`, `description` und `ownedBy` ergänzen. `ownedBy` enthält eine Liste von Organisationskennungen als Objekte.
- `keywords` enthält Stichwörter mit einem mehrsprachigen `label` und bei Bedarf einer `uri` zum Begriff. [TERMDAT](https://www.termdat.bk.admin.ch/) · [GEMET](https://www.eionet.europa.eu/gemet/)
- `isDescribedAt` verweist auf beschreibende Datensätze, `relations` auf verwandte Behördenleistungen und `requires` auf vorausgesetzte Behördenleistungen. Erfasse vorhandene Ressourcen der Zielumgebung als `{"id": "<I14Y-UUID>"}`.
- `responsiblePerson` und `responsibleDeputy` verwenden jeweils ein Objekt mit `email`. Da die Quelldatei im Repository sichtbar ist, erfasse nur E-Mail-Adressen, die dort stehen dürfen.

Beim Übernehmen eines I14Y-Exports reduziere Codelistenobjekte auf `code` und den Herausgeber auf `identifier`. Lass die Exportfelder `system`, `publicationLevel` und `registrationStatus` weg. Die Schreibmodelle `PublicServiceInputModel` und `ChannelInputModel` dokumentieren die API-Felder. [I14Y Partner API – Swagger](https://apiconsole.i14y.admin.ch/partner/v1/index.html) · [OpenAPI-Datei](https://apiconsole.i14y.admin.ch/partner/v1/Release.json)

## Prüfen und übermitteln

Führe vom Repository-Stamm aus folgenden Befehl aus, um die JSON-Struktur und die vom Harvester verlangten Pflichtangaben lokal zu prüfen. I14Y prüft die Gültigkeit der Codelistenwerte und Referenzen bei der Übermittlung.

```bash
python -m i14y.publicservices.harvester
```

Starte anschliessend den gewünschten manuellen Workflow. Er legt neue Einträge an und aktualisiert bestehende anhand ihrer ersten Kennung. [Public Services ABN](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_abn.yml) · [Public Services PROD](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_prod.yml)
