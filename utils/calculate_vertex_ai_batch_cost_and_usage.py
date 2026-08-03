from typing import List, Optional, Tuple

def calculate_vertex_ai_batch_cost_and_usage(
    vertex_ai_batch_responses: List[dict],
    model_name: Optional[str] = None,
) -> Tuple[float, Usage]:
    """
    Calculate both cost and usage from raw Vertex AI batch responses.

    Used only when ``litellm.disable_vertex_batch_output_transformation = True``.
    In that case the GCS predictions.jsonl is returned as-is, with each line in
    the native Vertex format:

      {"request": ..., "response": {"candidates": [...], "usageMetadata": {...}}}

    usageMetadata contains promptTokenCount, candidatesTokenCount, totalTokenCount.
    """
    from litellm.cost_calculator import batch_cost_calculator

    total_cost = 0.0
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    actual_model_name = model_name or "gemini-2.0-flash-001"

    for response in vertex_ai_batch_responses:
        response_body = response.get("response")
        if response_body is None:
            continue

        usage_metadata = response_body.get("usageMetadata", {})
        _prompt = usage_metadata.get("promptTokenCount", 0) or 0
        _completion = usage_metadata.get("candidatesTokenCount", 0) or 0
        _total = usage_metadata.get("totalTokenCount", 0) or (_prompt + _completion)

        line_usage = Usage(
            prompt_tokens=_prompt,
            completion_tokens=_completion,
            total_tokens=_total,
        )

        try:
            p_cost, c_cost = batch_cost_calculator(
                usage=line_usage,
                model=actual_model_name,
                custom_llm_provider="vertex_ai",
            )
            total_cost += p_cost + c_cost
        except Exception as e:
            verbose_logger.debug(
                "vertex_ai batch cost calculation error for line: %s", str(e)
            )

        prompt_tokens += _prompt
        completion_tokens += _completion
        total_tokens += _total

    verbose_logger.info(
        "vertex_ai batch cost: cost=%s, prompt=%d, completion=%d, total=%d",
        total_cost,
        prompt_tokens,
        completion_tokens,
        total_tokens,
    )

    return total_cost, Usage(
        total_tokens=total_tokens,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

