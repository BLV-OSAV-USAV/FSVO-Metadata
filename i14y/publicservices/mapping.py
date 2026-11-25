def get_field_mapping(service):
    """Wrap an I14Y public service input object for the Partner API."""
    if not isinstance(service, dict):
        raise ValueError("Jede öffentliche Leistung muss ein JSON-Objekt sein.")
    identifiers = service.get('identifiers')
    if not isinstance(identifiers, list) or not identifiers or not all(
        isinstance(identifier, str) and identifier.strip() for identifier in identifiers
    ):
        raise ValueError("Eine öffentliche Leistung braucht eine stabile Kennung in identifiers.")
    for field in ('name', 'description'):
        if not any(isinstance(text, str) and text.strip()
                   for text in (service.get(field) or {}).values()):
            raise ValueError(f"{identifiers[0]}: {field} benötigt mindestens einen Text.")
    if not (service.get('publisher') or {}).get('identifier'):
        raise ValueError(f"{identifiers[0]}: publisher.identifier fehlt.")
    return {'data': service}
