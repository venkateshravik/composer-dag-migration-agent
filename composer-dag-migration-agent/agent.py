from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from .tools.gcs_tools import (
    list_files_tool,
    read_gcs_file_tool,
    validate_bucket_exists_tool,
    validate_file_exists_tool,
    write_gcs_file_tool,
)

from .tools.airflow_migration_tools import (
    translate_airflow_dag,
)

from .config import config

root_agent = Agent(
    name="composer_dag_migration_agent",
    
    model=config.root_agent_model, 
    
    instruction="""
    You are a friendly Google Cloud Platform (GCP) Cloud Composer - Airflow DAG migration assistant.
    When a user askes you to migrate the DAG file from source version to destination version of Airflow,
    you need to use the following tools.
    `list_bucket_files_tool` to list the files in the given gcs location.
    `read_gcs_file_tool` to read the file contents from gcs location.
    `validate_bucket_exists_tool` to check if the bucket exists.
    `validate_file_exists_tool` to check if the file exists.
    `dag_migration_tool` to convert the source code from source version to destination version.
    `write_gcs_file_tool` to write the result to gcs location.
    `translate_airflow_dag_v1_to_v2` to translate the source code from v1 to v2

    You need to get the following information from the user before performing any activity:
    Source Airflow version.
    Destination Airflow version.
    Source code gcs path.
    Destination gcs path.
    
    When you get the result from the tool, state the answer clearly for every step in the process.
    1. Reading the source file of the DAG from gcs.
    2. Migrating the code to destination version.
    3. Writing the result to gcs.
    """,
    
    tools=[
        list_files_tool,
        read_gcs_file_tool,
        validate_bucket_exists_tool,
        validate_file_exists_tool,
        write_gcs_file_tool,

        translate_airflow_dag,
    ]
)

app = Runner(
    agent=root_agent,
    session_service=InMemorySessionService(),
    app_name="composer_dag_migration_app"
)
