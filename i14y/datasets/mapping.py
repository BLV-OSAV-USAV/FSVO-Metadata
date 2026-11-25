import calendar
import datetime
import re

from i14y import config


# Crosswalk from the FSVO catalogue vocabulary to the I14Y theme codes.
THEME_CODES = {
    "administration": "119",
    "agriculture": "109",
    "education": "103",
    "health": "114",
    "industry": "115",
    "national-economy": "115",
    "research": "103",
    "territory": "102",
    "trade": "115",
}


def coverage_timestamp(value, *, end=False):
    """Normalize catalogue dates to offset timestamps; expand partial date bounds."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    text = str(value).strip()
    # The source catalogue also uses year-first dates with slash separators.
    if re.fullmatch(r"\d{4}/\d{2}(?:/\d{2})?", text):
        text = text.replace('/', '-')
    if re.fullmatch(r"\d{4}(?:-\d{2})?", text):
        parts = text.split('-')
        year = int(parts[0])
        month = int(parts[1]) if len(parts) == 2 else (12 if end else 1)
        day = calendar.monthrange(year, month)[1] if end else 1
        timestamp = datetime.datetime(year, month, day)
    else:
        timestamp = datetime.datetime.fromisoformat(text.replace('Z', '+00:00'))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
    return timestamp.isoformat()


def localized_text(values):
    return {lang: text.strip() for lang, text in values.items()
            if lang in {'de', 'en', 'fr', 'it', 'rm'}
            and isinstance(text, str) and text.strip()}


def get_field_mapping(dataset):
    """Map a processed FSVO catalogue record to an I14Y dataset payload."""
    rights = dataset['dct:accessRights'].strip()
    access_codes = {'OPEN': 'PUBLIC', 'SENSITIVE': 'NON_PUBLIC'}
    privacy_codes = {
        'none': 'no_person',
        'personalData': 'person',
        'sensitivePersonalData': 'protect_person',
    }
    title = localized_text(dataset['dct:title'])
    description = localized_text(dataset['dct:description'])
    data = {
        'identifiers': [dataset['dct:identifier']],
        'title': title,
        'description': description,
        'publisher': config.DEFAULT_PUBLISHER.copy(),
        'accessRights': {'code': access_codes.get(rights, rights)},
        'confidentialityPerson': {'code': privacy_codes[dataset['bv:personalData']]},
        'keywords': [
            {'label': {'de': keyword.strip()}}
            for keyword in dataset.get('dcat:keyword', [])
            if isinstance(keyword, str) and keyword.strip()
        ],
        'distributions': [],
    }

    for field in ('issued', 'modified'):
        if timestamp := coverage_timestamp(dataset.get(f'dct:{field}')):
            data[field] = timestamp

    if landing_page := dataset.get('dcat:landingPage'):
        data['landingPages'] = [{'uri': landing_page}]

    if image := dataset.get('schema:image'):
        data['images'] = [{'uri': image}]

    spatial = (dataset.get('dct:spatial') or '').strip()
    if spatial and spatial.lower() not in {'no', 'yes'}:
        data['spatial'] = [spatial]

    theme_codes = {}
    for group in dataset.get('dcat:theme') or []:
        for value in group.split(','):
            theme = value.strip().lower()
            if theme == 'nantional-economy':
                theme = 'national-economy'
            if theme in THEME_CODES:
                theme_codes[THEME_CODES[theme]] = None
    if theme_codes:
        data['themes'] = [{'code': code} for code in theme_codes]

    contact = dataset.get('dcat:contactPoint') or {}
    if email := contact.get('schema:email'):
        point = {'kind': 'Organization', 'hasEmail': email}
        if name := contact.get('schema:name'):
            point['fn'] = {'de': name}
        data['contactPoints'] = [point]

    period = dataset.get('dct:temporal') or {}
    coverage = {
        'start': coverage_timestamp(period.get('dcat:start_date')),
        'end': coverage_timestamp(period.get('dcat:end_date'), end=True),
    }
    if any(coverage.values()):
        data['temporalCoverage'] = [coverage]

    for distribution in dataset.get('dcat:distribution') or []:
        if access_url := distribution.get('dcat:accessURL'):
            item = {
                'accessUrl': {'uri': access_url},
                'title': localized_text(distribution.get('dct:title') or {}) or title,
                'description': localized_text(distribution.get('dct:description') or {}) or description,
            }
            if identifier := distribution.get('dct:identifier'):
                item['identifier'] = identifier
            if 'temporalCoverage' in data:
                item['coverage'] = [coverage.copy()]
            data['distributions'].append(item)

    return {'data': data}
