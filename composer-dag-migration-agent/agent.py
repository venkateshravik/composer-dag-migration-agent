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


root_agent = Agent(
    name="composer_dag_migration_agent",
    
    # You can use any compatible model.
    # ADK uses LiteLLM to connect to various models.
    model="gemini-2.5-flash", 
    
    # The instructions are key. We tell the agent *how* to behave
    # and to *use its tools* for math.
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
    
    # This is where you give the agent its capabilities
    tools=[
        list_files_tool,
        read_gcs_file_tool,
        validate_bucket_exists_tool,
        validate_file_exists_tool,
        write_gcs_file_tool,

        translate_airflow_dag,
    ]
)

# --- Step 3: Configure the Agent Runner (Boilerplate) ---
# This sets up your agent to be runnable and to remember
# conversations in memory.

app = Runner(
    agent=root_agent,
    session_service=InMemorySessionService(),
    app_name="composer_dag_migration_app"
)

# This part allows the file to be run directly by Python
# for testing in your terminal.
if __name__ == "__main__":
    import asyncio

    async def run_test():
        print("Starting agent... (Type 'exit' to quit)")
        session = await app.async_create_session(user_id="test-user")
        
        while True:
            query_text = input("You: ")
            if query_text.lower() == "exit":
                break
            
            print("Agent:", end=" ", flush=True)
            
            # This streams the agent's response
            async for event in app.async_stream_query(
                session_id=session.id,
                user_id=session.user_id,
                message=query_text
            ):
                if event.type == "text":
                    print(event.text, end="", flush=True)
            
            print("\n") # Newline after agent is done

    asyncio.run(run_test())