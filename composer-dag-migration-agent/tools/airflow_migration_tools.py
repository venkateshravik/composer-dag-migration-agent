import vertexai
from vertexai.generative_models import GenerativeModel

from ..translator_system_prompt import v1_to_v2_system_prompt, v1_to_v3_system_prompt
from ..config import config


def translate_airflow_dag(v1_code: str, destination_airflow_version: str) -> dict:
    """
    Translates a block of Airflow v1 DAG code into Airflow v2/v3 compatible code.

    Args:
        v1_code: A string containing the complete Airflow v1 Python code.

    Returns:
        A dictionary containing the translated code.
    """
    try:
        TRANSLATOR_SYSTEM_PROMPT = None
        if destination_airflow_version == "v2":
            TRANSLATOR_SYSTEM_PROMPT = v1_to_v2_system_prompt
        elif destination_airflow_version == "v3":
            TRANSLATOR_SYSTEM_PROMPT = v1_to_v3_system_prompt
        else:
            raise ValueError(f"Unsupported destination version: {destination_airflow_version}")

        model = GenerativeModel(
            config.generative_model,
            system_instruction=TRANSLATOR_SYSTEM_PROMPT
        )
        
        response = model.generate_content(v1_code)
        
        return {"translated_code": response.text}
    
    except Exception as e:
        print(f"Error during translation: {e}")
        return {"error": str(e)}