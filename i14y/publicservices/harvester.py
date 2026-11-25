import argparse
import json

from i14y import config
from .mapping import get_field_mapping


def main():
    parser = argparse.ArgumentParser(description="Öffentliche Leistungen für I14Y einlesen.")
    parser.add_argument('--apply', action='store_true', help="Einträge an I14Y übermitteln.")
    args = parser.parse_args()

    with config.PUBLIC_SERVICES_DATA_PATH.open(encoding='utf-8') as source:
        services = json.load(source)
    if not isinstance(services, list):
        raise ValueError("Die JSON-Quelle muss eine Liste öffentlicher Leistungen enthalten.")
    payloads = {}
    for service in services:
        payload = get_field_mapping(service)
        identifier = service['identifiers'][0]
        if identifier in payloads:
            raise ValueError(f"Doppelte Kennung in der lokalen Quelle: {identifier}")
        payloads[identifier] = payload

    print(f"{len(payloads)} öffentliche Leistungen eingelesen.")
    if not args.apply or not payloads:
        return

    from i14y.client import I14YClient

    client = I14YClient()
    for identifier, payload in payloads.items():
        target = client.find('publicservices', 'publicServiceIdentifier', identifier)
        if target is None:
            client.request('POST', 'publicservices', json=payload)
            print(f"Auf I14Y erstellt: {identifier}")
        else:
            client.request('PUT', f"publicservices/{target['id']}", json=payload)
            print(f"Auf I14Y aktualisiert: {identifier}")


if __name__ == '__main__':
    main()
