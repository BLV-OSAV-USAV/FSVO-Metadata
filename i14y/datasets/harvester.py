import datetime
import json

from i14y import config
from i14y.client import I14YClient
from .mapping import coverage_timestamp, get_field_mapping


def publish_and_register_i14y(client, dataset_id, current):
    """Complete publication, including after a partially successful run."""
    if current.get('publicationLevel') != 'Public':
        client.set_state(f'datasets/{dataset_id}/publication-level', 'level', 'Public', 'publication level')
    if current.get('registrationStatus') != 'Recorded':
        client.set_state(f'datasets/{dataset_id}/registration-status', 'status', 'Recorded', 'registration status')


if __name__ == "__main__":

    client = I14YClient()

    with config.HARVEST_DATA_PATH.open(encoding='utf-8') as source:
        catalog = json.load(source)

    utc_plus_1 = datetime.timezone(datetime.timedelta(hours=1))
    cutoff = datetime.datetime.now(utc_plus_1) - datetime.timedelta(days=31)
    rows = [
        row for row in catalog
        if row.get('dct:identifier') in config.I14Y_DATASET_IDENTIFIERS
    ]

    created_datasets = []
    updated_datasets = []
    unchanged_datasets = []
    failure = None
    selection_summary = (
        f"Katalog: {len(rows)} von {len(catalog)} Datensätzen für I14Y ausgewählt; "
        f"Stichtag: {cutoff.isoformat()}"
    )
    print(selection_summary)

    try:
        for row in rows:
            identifier = row['dct:identifier']
            dates = [
                datetime.datetime.fromisoformat(timestamp)
                for field in ('dct:issued', 'dct:modified')
                if (timestamp := coverage_timestamp(row.get(field))) is not None
            ]
            print(f"Prüfe {identifier}: erstellt={row.get('dct:issued')}, geändert={row.get('dct:modified')}")

            target = client.find('datasets', 'datasetIdentifier', identifier)
            if target is not None and dates and max(dates) <= cutoff:
                publish_and_register_i14y(client, target['id'], target)
                unchanged_datasets.append(identifier)
                print(f"Bereits auf I14Y vorhanden und unverändert: {identifier} (I14Y-ID: {target['id']})")
                continue

            payload = get_field_mapping(row)
            if target is None:
                client.request('POST', 'datasets', json=payload)
                created_datasets.append(identifier)
                print(f"Auf I14Y erstellt: {identifier}")
                # Resolve the new ID rather than using an unrelated previous ID.
                target = client.find('datasets', 'datasetIdentifier', identifier)
                if target is None:
                    raise RuntimeError(f"{identifier} wurde erstellt, ist aber noch nicht auffindbar; Publikation und Registrierung konnten nicht gesetzt werden.")
            else:
                client.request('PUT', f"datasets/{target['id']}", json=payload)
                updated_datasets.append(identifier)
                print(f"Auf I14Y aktualisiert: {identifier} (I14Y-ID: {target['id']})")
            publish_and_register_i14y(client, target['id'], target)
            print(f"Auf I14Y publiziert und registriert: {identifier} (I14Y-ID: {target['id']})")

    except Exception as error:
        failure = f"Fehler bei {identifier}: {error}"
        raise
    finally:
        # Print the same report that is uploaded as an artifact.
        sections = [
            ("Auf I14Y erstellt", created_datasets),
            ("Auf I14Y aktualisiert", updated_datasets),
            ("Bereits auf I14Y vorhanden und unverändert", unchanged_datasets),
        ]
        lines = [
            "Harvest fehlgeschlagen" if failure else "Harvest abgeschlossen",
            selection_summary,
            f"Auf I14Y geladen: {len(created_datasets) + len(updated_datasets)}",
        ]
        if failure:
            lines.append(failure)
        for label, identifiers in sections:
            lines.append(f"\n{label} ({len(identifiers)}):")
            lines.extend(f"- {identifier}" for identifier in identifiers)
        log = "\n".join(lines) + "\n"
        print(log)
        with open('harvest_log.txt', 'w') as f:
            f.write(log)
