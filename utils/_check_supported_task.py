
def _check_supported_task(model: str, task: str) -> None:
    from huggingface_hub.hf_api import HfApi

    model_info = HfApi().model_info(model)
    pipeline_tag = model_info.pipeline_tag
    tags = model_info.tags or []
    is_conversational = "conversational" in tags
    if task in ("text-generation", "conversational"):
        if pipeline_tag == "text-generation":
            # text-generation + conversational tag -> both tasks allowed
            if is_conversational:
                return
            # text-generation without conversational tag -> only text-generation allowed
            if task == "text-generation":
                return
            raise ValueError(f"Model '{model}' doesn't support task '{task}'.")

    if pipeline_tag == "text2text-generation":
        if task == "text-generation":
            return
        raise ValueError(f"Model '{model}' doesn't support task '{task}'.")

    if pipeline_tag == "image-text-to-text":
        if is_conversational and task == "conversational":
            return  # Only conversational allowed if tagged as conversational
        raise ValueError("Non-conversational image-text-to-text task is not supported.")

    if (
        task in ("feature-extraction", "sentence-similarity")
        and pipeline_tag in ("feature-extraction", "sentence-similarity")
        and task in tags
    ):
        # feature-extraction and sentence-similarity are interchangeable for HF Inference
        return

    # For all other tasks, just check pipeline tag
    if pipeline_tag != task:
        raise ValueError(
            f"Model '{model}' doesn't support task '{task}'. Supported tasks: '{pipeline_tag}', got: '{task}'"
        )
    return

