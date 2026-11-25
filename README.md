🚧 **This project is currently under active development!**  
⚠️ **All data is arbitrary and for testing purposes only.** 



[![Combine Datasets](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/combine-datasets.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/combine-datasets.yml)
[![I14Y datasets ABN](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_abn.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_abn.yml)
[![I14Y datasets PROD](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_prod.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_prod.yml)
[![I14Y public services ABN](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_abn.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_abn.yml)
[![I14Y public services PROD](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_prod.yml/badge.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/actions/workflows/harvester_publicservices_prod.yml)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-ND 4.0](https://img.shields.io/badge/License-CC%20BY--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nd/4.0/)
[![GitHub last commit](https://img.shields.io/github/last-commit/BLV-OSAV-USAV/FSVO-Metadata.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/commits)
[![GitHub issues](https://img.shields.io/github/issues/BLV-OSAV-USAV/FSVO-Metadata.svg)](https://github.com/BLV-OSAV-USAV/FSVO-Metadata/issues)

Welcome to the **FSVO Metadata** repository! Here, you'll find the metadata files that describe various datasets of ours, the Python automation script responsible for merging and validating our metadata files, as well as the JSON Schemas that ensure each record follows a consistent format. Under `data/processed`, we store the combined metadata ready for use in the FOAG Data Catalog. This setup helps maintain high-quality, well-structured metadata that is compatible with both [I14Y](https://www.i14y.admin.ch/) and [opendata.swiss](https://opendata.swiss).

The metadata you find here is displayed in a more user-friendly way by our [data catalog](https://github.com/blw-ofag-ufag/data-catalog) web application.

## I14Y metadata harvesting

The harvesters in [`i14y/`](i14y/) send dataset and public service metadata to the I14Y Partner API. Each resource type has separate GitHub Actions workflows for ABN (acceptance) and PROD (production).

- **Datasets** are read from [`data/processed/datasets.json`](data/processed/datasets.json), which the Combine Datasets workflow generates. Set `I14Y_DATASET_IDENTIFIERS` in [`i14y/config.py`](i14y/config.py) to the `dct:identifier` values to harvest. An empty set selects zero datasets.
- **Public services** are read from [`data/publicservices/publicservices.json`](data/publicservices/publicservices.json). Add entries using the [example JSON](data/publicservices/publicservices.example.json) as a template. Keep each service's first identifier stable so the harvester can find and update the existing I14Y entry. [Public services entry guide](data/publicservices/README.md)

The public services template uses the I14Y write format. Use objects such as `{"code": "de"}` for coded fields and `{"identifier": "CH_BLV"}` for publisher and channel owners. For `isDescribedAt`, `relations` and `requires`, use `{"id": "<I14Y UUID>"}` for an existing I14Y resource. Replace the example URL, email addresses and codes with values for the service, or omit optional fields that do not apply. [I14Y Partner API write schema](https://apiconsole.i14y.admin.ch/partner/v1/Release.json)

To check the public service input locally, run `python -m i14y.publicservices.harvester` from the repository root. This checks the input structure and required fields. API writes require `--apply` and an `ACCESS_TOKEN`. Local runs target ABN by default. Set `I14Y_ENVIRONMENT=PROD` to target production.

### GitHub Actions and logs

Use **Run workflow** on the corresponding Actions page to start any of the four harvesters manually. The PROD dataset workflow also runs on Mondays at 03:00 UTC. Each workflow uses its environment's I14Y client ID and client secret from GitHub Actions secrets.

The workflows upload harvest logs as artifacts. After a successful branch run, the workflow also commits the latest log to `logs/i14y/<harvester>/<environment>/latest.txt` on that branch. Each run replaces the previous log at that path. Older versions are available in Git history.
