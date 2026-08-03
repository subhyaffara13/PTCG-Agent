from typing import Optional

def _strip_model_name(model: str, custom_llm_provider: Optional[str]) -> str:
    if custom_llm_provider and custom_llm_provider in ["bedrock", "bedrock_converse"]:
        stripped_bedrock_model = _get_base_bedrock_model(model_name=model)
        return stripped_bedrock_model
    elif custom_llm_provider and (
        custom_llm_provider == "vertex_ai" or custom_llm_provider == "gemini"
    ):
        strip_version = _strip_stable_vertex_version(model_name=model)
        return strip_version
    elif custom_llm_provider and (custom_llm_provider == "databricks"):
        strip_version = _strip_stable_vertex_version(model_name=model)
        return strip_version
    elif "ft:" in model:
        strip_finetune = _strip_openai_finetune_model_name(model_name=model)
        return strip_finetune
    else:
        return model

