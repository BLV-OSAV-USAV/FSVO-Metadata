import os
from pathlib import Path

###########################################
#Harvesting FILE 
###########################################

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
HARVEST_DATA_PATH = DATA_DIR / "processed" / "datasets.json"
PUBLIC_SERVICES_DATA_PATH = DATA_DIR / "publicservices" / "publicservices.json"

# Nur diese dct:identifier für I14Y berücksichtigen. Eine leere Liste übermittelt nichts.
I14Y_DATASET_IDENTIFIERS: set[str] = {
     "FSVO_D00001",
}

###########################################
# I14Y API configuration
###########################################

API_BASE_URLS = {
    "ABN": "https://api-a.i14y.admin.ch/api/partner/v1/",
    "PROD": "https://api.i14y.admin.ch/api/partner/v1/",
}
API_BASE_URL = API_BASE_URLS[os.environ.get("I14Y_ENVIRONMENT", "ABN")]

# Organization settings
ORGANIZATION_ID = "CH_BLV"
DEFAULT_PUBLISHER = {
    "identifier": ORGANIZATION_ID
}


