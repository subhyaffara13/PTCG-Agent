from typing import Tuple

def _handle_128k_pricing(
    model_info: ModelInfo,
    usage: Usage,
) -> Tuple[float, float]:
    ## CALCULATE INPUT COST
    input_cost_per_token_above_128k_tokens = model_info.get(
        "input_cost_per_token_above_128k_tokens"
    )
    output_cost_per_token_above_128k_tokens = model_info.get(
        "output_cost_per_token_above_128k_tokens"
    )

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    if (
        _is_above_128k(tokens=prompt_tokens)
        and input_cost_per_token_above_128k_tokens is not None
    ):
        prompt_cost = prompt_tokens * input_cost_per_token_above_128k_tokens
    else:
        prompt_cost = prompt_tokens * (model_info["input_cost_per_token"] or 0.0)

    ## CALCULATE OUTPUT COST
    output_cost_per_token_above_128k_tokens = model_info.get(
        "output_cost_per_token_above_128k_tokens"
    )
    if (
        _is_above_128k(tokens=completion_tokens)
        and output_cost_per_token_above_128k_tokens is not None
    ):
        completion_cost = completion_tokens * output_cost_per_token_above_128k_tokens
    else:
        completion_cost = completion_tokens * (
            model_info["output_cost_per_token"] or 0.0
        )

    return prompt_cost, completion_cost

