
def _get_batch_job_cost_from_file_content(
    file_content_dictionary: List[dict],
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "hosted_vllm", "anthropic"
    ] = "openai",
    model_info: Optional[ModelInfo] = None,
) -> float:
    """
    Get the cost of a batch job from the file content
    """
    from litellm.cost_calculator import batch_cost_calculator

    try:
        total_cost: float = 0.0
        # parse the file content as json
        verbose_logger.debug(
            "file_content_dictionary=%s", json.dumps(file_content_dictionary, indent=4)
        )
        for _item in file_content_dictionary:
            if _batch_response_was_successful(_item):
                _response_body = _get_response_from_batch_job_output_file(_item)
                if model_info is not None:
                    usage = _get_batch_job_usage_from_response_body(_response_body)
                    model = _response_body.get("model", "")
                    prompt_cost, completion_cost = batch_cost_calculator(
                        usage=usage,
                        model=model,
                        custom_llm_provider=custom_llm_provider,
                        model_info=model_info,
                    )
                    total_cost += prompt_cost + completion_cost
                else:
                    total_cost += litellm.completion_cost(
                        completion_response=_response_body,
                        custom_llm_provider=custom_llm_provider,
                        call_type=CallTypes.aretrieve_batch.value,
                    )
                verbose_logger.debug("total_cost=%s", total_cost)
        return total_cost
    except Exception as e:
        verbose_logger.error("error in _get_batch_job_cost_from_file_content", e)
        raise e

