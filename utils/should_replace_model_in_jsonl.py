
def should_replace_model_in_jsonl(
    purpose: OpenAIFilesPurpose,
) -> bool:
    """
    Check if the model name should be replaced in the JSONL file for the deployment model name.

    Azure raises an error on create batch if the model name for deployment is not in the .jsonl.
    """
    if purpose == "batch":
        return True
    return False

