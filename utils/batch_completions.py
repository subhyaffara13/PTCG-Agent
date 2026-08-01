
def batch_completions(
    model: str, messages: list, optional_params=None, custom_prompt_dict={}
):
    """
    Example usage:
    import litellm
    import os
    from litellm import batch_completion


    responses = batch_completion(
        model="vllm/facebook/opt-125m",
        messages = [
            [
                {
                    "role": "user",
                    "content": "good morning? "
                }
            ],
            [
                {
                    "role": "user",
                    "content": "what's the time? "
                }
            ]
        ]
    )
    """
    try:
        llm, SamplingParams = validate_environment(model=model)
    except Exception as e:
        error_str = str(e)
        raise VLLMError(status_code=0, message=error_str)
    sampling_params = SamplingParams(**optional_params)
    prompts = []
    if model in custom_prompt_dict:
        # check if the model has a registered custom prompt
        model_prompt_details = custom_prompt_dict[model]
        for message in messages:
            prompt = custom_prompt(
                role_dict=model_prompt_details["roles"],
                initial_prompt_value=model_prompt_details["initial_prompt_value"],
                final_prompt_value=model_prompt_details["final_prompt_value"],
                messages=message,
            )
            prompts.append(prompt)
    else:
        for message in messages:
            prompt = prompt_factory(model=model, messages=message)
            prompts.append(prompt)

    if llm:
        outputs = llm.generate(prompts, sampling_params)
    else:
        raise VLLMError(
            status_code=0, message="Need to pass in a model name to initialize vllm"
        )

    final_outputs = []
    for output in outputs:
        model_response = ModelResponse()
        ## RESPONSE OBJECT
        model_response.choices[0].message.content = output.outputs[0].text  # type: ignore

        ## CALCULATING USAGE
        prompt_tokens = len(output.prompt_token_ids)
        completion_tokens = len(output.outputs[0].token_ids)

        model_response.created = int(time.time())
        model_response.model = model
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        setattr(model_response, "usage", usage)
        final_outputs.append(model_response)
    return final_outputs

