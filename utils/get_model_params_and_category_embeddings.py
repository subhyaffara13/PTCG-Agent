import re

def get_model_params_and_category_embeddings(model_name) -> str:
    """
    Helper function for calculating together ai embedding pricing.

    Returns
    - str - model pricing category if mapped else received model name
    """
    model_name = model_name.lower()
    re_params_match = re.search(
        r"(\d+m)", model_name
    )  # catch all decimals like 100m, 200m, etc.
    category = None
    if re_params_match is not None:
        params_match = str(re_params_match.group(1))
        params_match = params_match.replace("m", "")
        if params_match is not None:
            params_million = float(params_match)
        else:
            return model_name
        # Determine the category based on the number of parameters
        if params_million <= TOGETHER_AI_EMBEDDING_150_M:
            category = "together-ai-embedding-up-to-150m"
        elif params_million <= TOGETHER_AI_EMBEDDING_350_M:
            category = "together-ai-embedding-151m-to-350m"
        if category is not None:
            return category

    return model_name

