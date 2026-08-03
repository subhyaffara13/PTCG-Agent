from typing import Optional, Tuple

def cost_per_character(
    model: str,
    custom_llm_provider: str,
    usage: Usage,
    prompt_characters: Optional[float] = None,
    completion_characters: Optional[float] = None,
) -> Tuple[float, float]:
    """
    Calculates the cost per character for a given VertexAI model, input messages, and response object.

    Input:
        - model: str, the model name without provider prefix
        - custom_llm_provider: str, "vertex_ai-*"
        - prompt_characters: float, the number of input characters
        - completion_characters: float, the number of output characters

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd

    Raises:
        Exception if model requires >128k pricing, but model cost not mapped
    """
    model_info = litellm.get_model_info(
        model=model, custom_llm_provider=custom_llm_provider
    )

    ## GET MODEL INFO
    model_info = litellm.get_model_info(
        model=model, custom_llm_provider=custom_llm_provider
    )

    ## CALCULATE INPUT COST
    if prompt_characters is None:
        prompt_cost, _ = cost_per_token(
            model=model,
            custom_llm_provider=custom_llm_provider,
            usage=usage,
        )
    else:
        try:
            if (
                _is_above_128k(tokens=prompt_characters * 4)  # 1 token = 4 char
                and model not in models_without_dynamic_pricing
            ):
                ## check if character pricing, else default to token pricing
                assert (
                    "input_cost_per_character_above_128k_tokens" in model_info
                    and model_info["input_cost_per_character_above_128k_tokens"]
                    is not None
                ), "model info for model={} does not have 'input_cost_per_character_above_128k_tokens'-pricing for > 128k tokens\nmodel_info={}".format(
                    model, model_info
                )
                prompt_cost = (
                    prompt_characters
                    * model_info["input_cost_per_character_above_128k_tokens"]
                )
            else:
                assert (
                    "input_cost_per_character" in model_info
                    and model_info["input_cost_per_character"] is not None
                ), "model info for model={} does not have 'input_cost_per_character'-pricing\nmodel_info={}".format(
                    model, model_info
                )
                prompt_cost = prompt_characters * model_info["input_cost_per_character"]
        except Exception as e:
            verbose_logger.debug(
                "litellm.litellm_core_utils.llm_cost_calc.google.py::cost_per_character(): Exception occured - {}\nDefaulting to None".format(
                    str(e)
                )
            )
            prompt_cost, _ = cost_per_token(
                model=model,
                custom_llm_provider=custom_llm_provider,
                usage=usage,
            )

    ## CALCULATE OUTPUT COST
    if completion_characters is None:
        _, completion_cost = cost_per_token(
            model=model,
            custom_llm_provider=custom_llm_provider,
            usage=usage,
        )
    else:
        completion_tokens = usage.completion_tokens
        try:
            if (
                _is_above_128k(tokens=completion_characters * 4)  # 1 token = 4 char
                and model not in models_without_dynamic_pricing
            ):
                assert (
                    "output_cost_per_character_above_128k_tokens" in model_info
                    and model_info["output_cost_per_character_above_128k_tokens"]
                    is not None
                ), "model info for model={} does not have 'output_cost_per_character_above_128k_tokens' pricing\nmodel_info={}".format(
                    model, model_info
                )
                completion_cost = (
                    completion_tokens
                    * model_info["output_cost_per_character_above_128k_tokens"]
                )
            else:
                assert (
                    "output_cost_per_character" in model_info
                    and model_info["output_cost_per_character"] is not None
                ), "model info for model={} does not have 'output_cost_per_character'-pricing\nmodel_info={}".format(
                    model, model_info
                )
                completion_cost = (
                    completion_characters * model_info["output_cost_per_character"]
                )
        except Exception as e:
            verbose_logger.debug(
                "litellm.litellm_core_utils.llm_cost_calc.google.py::cost_per_character(): Exception occured - {}\nDefaulting to None".format(
                    str(e)
                )
            )
            _, completion_cost = cost_per_token(
                model=model,
                custom_llm_provider=custom_llm_provider,
                usage=usage,
            )

    return prompt_cost, completion_cost

