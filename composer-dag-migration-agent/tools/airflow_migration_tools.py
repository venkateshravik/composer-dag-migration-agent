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
        system_prompt_selector = {
            "v2": v1_to_v2_system_prompt,
            "v3": v1_to_v3_system_prompt
        }
        TRANSLATOR_SYSTEM_PROMPT = system_prompt_selector.get(destination_airflow_version)

        model = GenerativeModel(
            config.generative_model,
            system_instruction=TRANSLATOR_SYSTEM_PROMPT
        )
        
        response = model.generate_content(v1_code)

        lines = response.text.splitlines()
        cleaned_lines = lines[1:-1]
        cleaned_response = "\n".join(cleaned_lines)
        
        return {"translated_code": cleaned_response}
    
    except Exception as e:
        print(f"Error during translation: {e}")
        return {"error": str(e)}