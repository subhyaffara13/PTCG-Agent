from typing import Any, Dict, List, Optional, Union

def text_completion(
    prompt: Union[
        str, List[Union[str, List[Union[str, List[int]]]]]
    ],  # Required: The prompt(s) to generate completions for.
    model: Optional[str] = None,  # Optional: either `model` or `engine` can be set
    best_of: Optional[
        int
    ] = None,  # Optional: Generates best_of completions server-side.
    echo: Optional[
        bool
    ] = None,  # Optional: Echo back the prompt in addition to the completion.
    frequency_penalty: Optional[
        float
    ] = None,  # Optional: Penalize new tokens based on their existing frequency.
    logit_bias: Optional[
        Dict[int, int]
    ] = None,  # Optional: Modify the likelihood of specified tokens.
    logprobs: Optional[
        int
    ] = None,  # Optional: Include the log probabilities on the most likely tokens.
    max_tokens: Optional[
        int
    ] = None,  # Optional: The maximum number of tokens to generate in the completion.
    n: Optional[
        int
    ] = None,  # Optional: How many completions to generate for each prompt.
    presence_penalty: Optional[
        float
    ] = None,  # Optional: Penalize new tokens based on whether they appear in the text so far.
    stop: Optional[
        Union[str, List[str]]
    ] = None,  # Optional: Sequences where the API will stop generating further tokens.
    stream: Optional[bool] = None,  # Optional: Whether to stream back partial progress.
    stream_options: Optional[dict] = None,
    suffix: Optional[
        str
    ] = None,  # Optional: The suffix that comes after a completion of inserted text.
    temperature: Optional[float] = None,  # Optional: Sampling temperature to use.
    top_p: Optional[float] = None,  # Optional: Nucleus sampling parameter.
    user: Optional[
        str
    ] = None,  # Optional: A unique identifier representing your end-user.
    # set api_base, api_version, api_key
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    model_list: Optional[list] = None,  # pass in a list of api_base,keys, etc.
    # Optional liteLLM function params
    custom_llm_provider: Optional[str] = None,
    *args,
    **kwargs,
):
    import copy

    """
    Generate text completions using the OpenAI API.

    Args:
        model (str): ID of the model to use.
        prompt (Union[str, List[Union[str, List[Union[str, List[int]]]]]): The prompt(s) to generate completions for.
        best_of (Optional[int], optional): Generates best_of completions server-side. Defaults to 1.
        echo (Optional[bool], optional): Echo back the prompt in addition to the completion. Defaults to False.
        frequency_penalty (Optional[float], optional): Penalize new tokens based on their existing frequency. Defaults to 0.
        logit_bias (Optional[Dict[int, int]], optional): Modify the likelihood of specified tokens. Defaults to None.
        logprobs (Optional[int], optional): Include the log probabilities on the most likely tokens. Defaults to None.
        max_tokens (Optional[int], optional): The maximum number of tokens to generate in the completion. Defaults to 16.
        n (Optional[int], optional): How many completions to generate for each prompt. Defaults to 1.
        presence_penalty (Optional[float], optional): Penalize new tokens based on whether they appear in the text so far. Defaults to 0.
        stop (Optional[Union[str, List[str]]], optional): Sequences where the API will stop generating further tokens. Defaults to None.
        stream (Optional[bool], optional): Whether to stream back partial progress. Defaults to False.
        suffix (Optional[str], optional): The suffix that comes after a completion of inserted text. Defaults to None.
        temperature (Optional[float], optional): Sampling temperature to use. Defaults to 1.
        top_p (Optional[float], optional): Nucleus sampling parameter. Defaults to 1.
        user (Optional[str], optional): A unique identifier representing your end-user.
    Returns:
        TextCompletionResponse: A response object containing the generated completion and associated metadata.

    Example:
        Your example of how to use this function goes here.
    """
    if "engine" in kwargs:
        _engine = kwargs["engine"]
        if model is None and isinstance(_engine, str):
            # only use engine when model not passed
            model = _engine
        kwargs.pop("engine")

    text_completion_response = TextCompletionResponse()

    optional_params: Dict[str, Any] = {}
    # default values for all optional params are none, litellm only passes them to the llm when they are set to non None values
    if best_of is not None:
        optional_params["best_of"] = best_of
    if echo is not None:
        optional_params["echo"] = echo
    if frequency_penalty is not None:
        optional_params["frequency_penalty"] = frequency_penalty
    if logit_bias is not None:
        optional_params["logit_bias"] = logit_bias
    if logprobs is not None:
        optional_params["logprobs"] = logprobs
    if max_tokens is not None:
        optional_params["max_tokens"] = max_tokens
    if n is not None:
        optional_params["n"] = n
    if presence_penalty is not None:
        optional_params["presence_penalty"] = presence_penalty
    if stop is not None:
        optional_params["stop"] = stop
    if stream is not None:
        optional_params["stream"] = stream
    if stream_options is not None:
        optional_params["stream_options"] = stream_options
    if suffix is not None:
        optional_params["suffix"] = suffix
    if temperature is not None:
        optional_params["temperature"] = temperature
    if top_p is not None:
        optional_params["top_p"] = top_p
    if user is not None:
        optional_params["user"] = user
    if api_base is not None:
        optional_params["api_base"] = api_base
    if api_version is not None:
        optional_params["api_version"] = api_version
    if api_key is not None:
        optional_params["api_key"] = api_key
    if custom_llm_provider is not None:
        optional_params["custom_llm_provider"] = custom_llm_provider

    # get custom_llm_provider
    _model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
        model=model,  # type: ignore
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
    )

    if custom_llm_provider == "huggingface":
        # if echo == True, for TGI llms we need to set top_n_tokens to 3
        if echo is True:
            # for tgi llms
            if "top_n_tokens" not in kwargs:
                kwargs["top_n_tokens"] = 3

        # processing prompt - users can pass raw tokens to OpenAI Completion()
        if isinstance(prompt, list):
            import concurrent.futures

            tokenizer = tiktoken.encoding_for_model("text-davinci-003")
            ## if it's a 2d list - each element in the list is a text_completion() request
            if len(prompt) > 0 and isinstance(prompt[0], list):
                responses = [None for x in prompt]  # init responses

                def process_prompt(i, individual_prompt):
                    decoded_prompt = tokenizer.decode(individual_prompt)
                    all_params = {**kwargs, **optional_params}
                    response: TextCompletionResponse = text_completion(  # type: ignore
                        model=model,
                        prompt=decoded_prompt,
                        num_retries=3,  # ensure this does not fail for the batch
                        *args,
                        **all_params,
                    )

                    text_completion_response["id"] = response.get("id", None)
                    text_completion_response["object"] = "text_completion"
                    text_completion_response["created"] = response.get("created", None)
                    text_completion_response["model"] = response.get("model", None)
                    return response["choices"][0]

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    completed_futures = [
                        executor.submit(process_prompt, i, individual_prompt)
                        for i, individual_prompt in enumerate(prompt)
                    ]
                    for i, future in enumerate(
                        concurrent.futures.as_completed(completed_futures)
                    ):
                        responses[i] = future.result()
                    text_completion_response.choices = responses  # type: ignore

                return text_completion_response
    # else:
    # check if non default values passed in for best_of, echo, logprobs, suffix
    # these are the params supported by Completion() but not ChatCompletion

    # default case, non OpenAI requests go through here
    # handle prompt formatting if prompt is a string vs. list of strings
    messages = []
    if isinstance(prompt, list) and len(prompt) > 0 and isinstance(prompt[0], str):
        for p in prompt:
            message = {"role": "user", "content": p}
            messages.append(message)
    elif isinstance(prompt, str):
        messages = [{"role": "user", "content": prompt}]
    elif (
        (
            custom_llm_provider == "openai"
            or custom_llm_provider == "azure"
            or custom_llm_provider == "azure_text"
            or custom_llm_provider == "text-completion-codestral"
            or custom_llm_provider == "text-completion-openai"
        )
        and isinstance(prompt, list)
        and len(prompt) > 0
        and (isinstance(prompt[0], list) or isinstance(prompt[0], int))
    ):
        # Support for token IDs as prompt (list of integers or list of lists of integers)
        messages = [{"role": "user", "content": prompt}]  # type: ignore
    else:
        raise Exception(
            f"Unmapped prompt format. Your prompt is neither a list of strings nor a string. prompt={prompt}. File an issue - https://github.com/BerriAI/litellm/issues"
        )

    kwargs.pop("prompt", None)

    if _model is not None and (
        custom_llm_provider == "openai"
    ):  # for openai compatible endpoints - e.g. vllm, call the native /v1/completions endpoint for text completion calls
        if _model not in litellm.open_ai_chat_completion_models:
            model = "text-completion-openai/" + _model
            optional_params.pop("custom_llm_provider", None)

    if model is None:
        raise ValueError("model is not set. Set either via 'model' or 'engine' param.")
    kwargs["text_completion"] = True
    response = completion(
        model=model,
        messages=messages,
        *args,
        **kwargs,
        **optional_params,
    )
    if kwargs.get("acompletion", False) is True:
        return response
    if (
        stream is True
        or kwargs.get("stream", False) is True
        or isinstance(response, CustomStreamWrapper)
    ):
        response = TextCompletionStreamWrapper(
            completion_stream=response,
            model=model,
            stream_options=stream_options,
            custom_llm_provider=custom_llm_provider,
        )
        return response
    elif isinstance(response, TextCompletionStreamWrapper):
        return response

    # OpenAI Text / Azure Text will return here
    if isinstance(response, TextCompletionResponse):
        return response

    text_completion_response = (
        litellm.utils.LiteLLMResponseObjectHandler.convert_chat_to_text_completion(
            response=response,
            text_completion_response=text_completion_response,
        )
    )

    return text_completion_response

