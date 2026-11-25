import os
from pathlib import Path

###########################################
#Harvesting FILE 
###########################################

HARVEST_DATA_PATH = Path(__file__).resolve().parents[1] / "data/processed/datasets.json"

# Nur diese dct:identifier für I14Y berücksichtigen. Eine leere Liste übermittelt nichts.
I14Y_DATASET_IDENTIFIERS: set[str] = {
     "FSVO_D00001",
}

###########################################
# I14Y API configuration
###########################################

# API_BASE_URL = "https://api.i14y.admin.ch/api/partner/v1/" # Prod environement 
API_BASE_URL = "https://api-a.i14y.admin.ch/api/partner/v1/" # ABN enironement 
API_TOKEN = f"Bearer {os.environ['ACCESS_TOKEN']}" 

# Organization settings
ORGANIZATION_ID = "CH_BLV"
DEFAULT_PUBLISHER = {
    "identifier": ORGANIZATION_ID
}


