
def cost_per_second(
    model: str, custom_llm_provider: Optional[str], duration: float = 0.0
) -> Tuple[float, float]:
    """
    Calculates the cost per second for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - custom_llm_provider: str, the custom llm provider
        - duration: float, the duration of the response in seconds

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """

    ## GET MODEL INFO
    model_info = get_model_info(
        model=model, custom_llm_provider=custom_llm_provider or "openai"
    )
    prompt_cost = 0.0
    completion_cost = 0.0
    ## Speech / Audio cost calculation
    if (
        "output_cost_per_second" in model_info
        and model_info["output_cost_per_second"] is not None
    ):
        verbose_logger.debug(
            f"For model={model} - output_cost_per_second: {model_info.get('output_cost_per_second')}; duration: {duration}"
        )
        ## COST PER SECOND ##
        completion_cost = model_info["output_cost_per_second"] * duration
    elif (
        "input_cost_per_second" in model_info
        and model_info["input_cost_per_second"] is not None
    ):
        verbose_logger.debug(
            f"For model={model} - input_cost_per_second: {model_info.get('input_cost_per_second')}; duration: {duration}"
        )
        ## COST PER SECOND ##
        prompt_cost = model_info["input_cost_per_second"] * duration
        completion_cost = 0.0

    return prompt_cost, completion_cost

