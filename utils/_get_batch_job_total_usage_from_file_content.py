from typing import List, Optional

def _get_batch_job_total_usage_from_file_content(
    file_content_dictionary: List[dict],
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "hosted_vllm", "anthropic"
    ] = "openai",
    model_name: Optional[str] = None,
) -> Usage:
    """
    Get the tokens of a batch job from the file content
    """
    if (
        custom_llm_provider == "vertex_ai"
        and model_name
        and getattr(litellm, "disable_vertex_batch_output_transformation", False)
    ):
        _, batch_usage = calculate_vertex_ai_batch_cost_and_usage(
            file_content_dictionary, model_name
        )
        return batch_usage

    # For other providers, use the existing logic
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    for _item in file_content_dictionary:
        if _batch_response_was_successful(_item):
            _response_body = _get_response_from_batch_job_output_file(_item)
            usage: Usage = _get_batch_job_usage_from_response_body(_response_body)
            total_tokens += usage.total_tokens
            prompt_tokens += usage.prompt_tokens
            completion_tokens += usage.completion_tokens
    return Usage(
        total_tokens=total_tokens,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

