
def _batch_cost_calculator(
    file_content_dictionary: List[dict],
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "hosted_vllm", "anthropic"
    ] = "openai",
    model_name: Optional[str] = None,
    model_info: Optional[ModelInfo] = None,
) -> float:
    """
    Calculate the cost of a batch based on the output file id
    """
    if (
        custom_llm_provider == "vertex_ai"
        and model_name
        and getattr(litellm, "disable_vertex_batch_output_transformation", False)
    ):
        batch_cost, _ = calculate_vertex_ai_batch_cost_and_usage(
            file_content_dictionary, model_name
        )
        verbose_logger.debug("vertex_ai_total_cost=%s", batch_cost)
        return batch_cost

    # For other providers, use the existing logic
    total_cost = _get_batch_job_cost_from_file_content(
        file_content_dictionary=file_content_dictionary,
        custom_llm_provider=custom_llm_provider,
        model_info=model_info,
    )
    verbose_logger.debug("total_cost=%s", total_cost)
    return total_cost

