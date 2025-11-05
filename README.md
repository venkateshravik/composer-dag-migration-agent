# composer-dag-migration-agent

## Overview

This agent reads dag code files from a Google Cloud Storage (GCS) bucket performs a code translation from Airflow v1 to v2 or v3 and writes the resulting DAG files to the destination Composer GCS bucket.

For details on GCP deployment, please read and follow the instructions at [`deploy/README.md`](deploy/README.md).

## Agent Details

### Key Features

- Composer airflow dag translation from source version v1 to the latest version of v2 and v3.
- Automated discovery of dag files in the Composer dag bucket and saving the files in the destination bucket.

### Architecture



### Example Agent Interaction

> **User:**
> Hi, how are you?

> **Agent:**
> Hello! I'm doing well, thank you. I'm here to assist you with migrating your Airflow DAG files.
> To get started, I'll need some information from you:
>
> * Source Airflow version (e.g., Airflow 1)
> * Destination Airflow version (e.g., Airflow 2)
> * Source DAG file GCS path (e.g., `gs://your-bucket/dags/my_dag_v1.py`)
> * Destination GCS path for the migrated DAG file (e.g., `gs://your-bucket/dags/my_dag_v2.py`)
>
> Once I have these details, I can help you with the migration process.

> **User:**
> I want to translate dags from Airflow v1 to v2.
> The v1 dags are present in folder `gs://composer_migration_agent/v1_dags` and the converted dags need to be written to `gs://composer_migration_agent/v2_dags`.

> **Agent:**
> Okay, the source bucket `composer_migration_agent` exists.
> Now, I'm listing the DAG files in the `v1_dags` folder:
> I found the following DAG files in `gs://composer_migration_agent/v1_dags`:
>
> * `v1_dags/bigquery_dag.py`
> * `v1_dags/dataproc_dag.py`
>
> I will now start the migration process for `v1_dags/bigquery_dag.py`.
>
> 1.  **Reading the source file of the DAG from GCS:**
>     The content of `v1_dags/bigquery_dag.py` has been successfully read.
>
> 2.  **Migrating the code to destination version:**
>     The DAG code for `bigquery_dag.py` has been successfully migrated to Airflow v2.
>
> 3.  **Writing the result to GCS:**
>     The migrated `bigquery_dag.py` has been successfully written to `gs://composer_migration_agent/v2_dags/bigquery_dag.py`.
>

> **Agent:**
> Now, let's move on to the next DAG file: `dataproc_dag.py`.
>
> 1.  **Reading the source file of the DAG from GCS:**
>     The content of `v1_dags/dataproc_dag.py` has been successfully read.
>
> 2.  **Migrating the code to destination version:**
>     I have received the analysis and the modernized code for `dataproc_dag.py`. I will now write the corrected code to the destination GCS path: `gs://composer_migration_agent/v2_dags/dataproc_dag.py`.
>
> 3.  **Writing the result to GCS:**
>     I have successfully migrated `dataproc_dag.py` from Airflow v1 to v2 and written it to `gs://composer_migration_agent/v2_dags/dataproc_dag.py`.
>

> **Agent:**
> All your DAG files from `gs://composer_migration_agent/v1_dags` have been successfully translated to Airflow v2 and saved in `gs://composer_migration_agent/v2_dags`.

> **Agent:**
> Let me know if you have any other DAGs you'd like to migrate!## Setup and Installation

### Prerequisites

- **Google Credentials:** You need a GCP project _or_ Gemini API key for local testing. You need a GCP project for deployment to Cloud Run.
- **UV:** Ensure that you have uv installed. If you don't already, please follow the installation instructions at [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).

### Project Setup

1. **Install dependencies in a virtual environment:** `make install`

1. **Run static code analysis:** `make check`

1. **Set up Environment Variables:** Create a file named `.env` and update values as needed.

	```bash
	# If using API key: ML Dev backend config.
	GOOGLE_API_KEY=YOUR_VALUE_HERE
	GOOGLE_GENAI_USE_VERTEXAI=false

	# If using Vertex on GCP: Vertex backend config
	GOOGLE_CLOUD_PROJECT=YOUR_VALUE_HERE
	GOOGLE_CLOUD_LOCATION=YOUR_VALUE_HERE
	GOOGLE_GENAI_USE_VERTEXAI=true
	```

1. **If you're using a GCP project, authenticate with GCP and enable VertexAI:**

	```bash
	gcloud auth login --update-adc
	gcloud config set project PROJECT_ID
	gcloud services enable aiplatform.googleapis.com
	```

You are now ready to start development on your project!

## Running the Agent

Run the agent(s) API server with the command: `make api_server`. The API server docs may be accessed at the `/docs` endpoint (e.g. [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)). For more information on local testing, visit [https://google.github.io/adk-docs/get-started/testing/](https://google.github.io/adk-docs/get-started/testing/).

Run the agent with the ADK Web UI with the command: `make web`

## Running Tests

Tests assess the overall executability of the agents. All tests are located under the `tests/` directory.

Run tests with the command `make test`
