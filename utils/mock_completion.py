import logging
import time
from typing import List, Optional, Union

def mock_completion(
    model: str,
    messages: List,
    stream: Optional[bool] = False,
    n: Optional[int] = None,
    mock_response: Optional[MOCK_RESPONSE_TYPE] = "This is a mock request",
    mock_tool_calls: Optional[List] = None,
    mock_timeout: Optional[bool] = False,
    logging=None,
    custom_llm_provider=None,
    timeout: Optional[Union[float, str, httpx.Timeout]] = None,
    **kwargs,
):
    """
    Generate a mock completion response for testing or debugging purposes.

    This is a helper function that simulates the response structure of the OpenAI completion API.

    Parameters:
        model (str): The name of the language model for which the mock response is generated.
        messages (List): A list of message objects representing the conversation context.
        stream (bool, optional): If True, returns a mock streaming response (default is False).
        mock_response (str, optional): The content of the mock response (default is "This is a mock request").
        mock_timeout (bool, optional): If True, the mock response will be a timeout error (default is False).
        timeout (float, optional): The timeout value to use for the mock response (default is None).
        **kwargs: Additional keyword arguments that can be used but are not required.

    Returns:
        litellm.ModelResponse: A ModelResponse simulating a completion response with the specified model, messages, and mock response.

    Raises:
        Exception: If an error occurs during the generation of the mock completion response.
    Note:
        - This function is intended for testing or debugging purposes to generate mock completion responses.
        - If 'stream' is True, it returns a response that mimics the behavior of a streaming completion.
    """
    try:
        is_acompletion = kwargs.get("acompletion") or False
        if mock_response is None:
            mock_response = "This is a mock request"

        _handle_mock_timeout(mock_timeout=mock_timeout, timeout=timeout, model=model)

        ## LOGGING
        if logging is not None:
            logging.pre_call(
                input=messages,
                api_key="mock-key",
            )

        if isinstance(mock_response, str) or isinstance(mock_response, Exception):
            _handle_mock_potential_exceptions(
                mock_response=mock_response,
                model=model,
                custom_llm_provider=custom_llm_provider,
            )

        mock_response = cast(
            Union[str, dict, ModelResponse, ModelResponseStream], mock_response
        )  # after this point, mock_response is a string, dict, ModelResponse, or ModelResponseStream
        if isinstance(mock_response, str) and mock_response.startswith(
            "Exception: mock_streaming_error"
        ):
            mock_response = litellm.MockException(
                message="This is a mock error raised mid-stream",
                llm_provider="anthropic",
                model=model,
                status_code=529,
            )
        time_delay = kwargs.get("mock_delay", None)
        if time_delay is not None and not is_acompletion:
            time.sleep(time_delay)

        if isinstance(mock_response, dict):
            return ModelResponse(**mock_response)

        if isinstance(mock_response, ModelResponse):
            if not stream:
                return mock_response
            # convert to ModelResponseStream
            mock_response = convert_model_response_to_streaming(mock_response)  # type: ignore

        model_response: Union[ModelResponse, ModelResponseStream] = ModelResponse()

        if stream is True:
            model_response = ModelResponseStream()
            # don't try to access stream object,
            if kwargs.get("acompletion", False) is True:
                return CustomStreamWrapper(
                    completion_stream=async_mock_completion_streaming_obj(
                        model_response, mock_response=mock_response, model=model, n=n
                    ),
                    model=model,
                    custom_llm_provider="openai",
                    logging_obj=logging,
                )
            return CustomStreamWrapper(
                completion_stream=mock_completion_streaming_obj(
                    model_response, mock_response=mock_response, model=model, n=n
                ),
                model=model,
                custom_llm_provider="openai",
                logging_obj=logging,
            )
        if isinstance(mock_response, litellm.MockException):
            raise mock_response
        # At this point, mock_response must be a string (all other types have been handled or returned early)
        mock_response = cast(str, mock_response)

        if n is None:
            model_response.choices[0].message.content = mock_response  # type: ignore
        else:
            _all_choices = []
            for i in range(n):
                _choice = litellm.utils.Choices(
                    index=i,
                    message=litellm.utils.Message(
                        content=mock_response, role="assistant"
                    ),
                )
                _all_choices.append(_choice)
            model_response.choices = _all_choices  # type: ignore
        model_response.created = int(time.time())
        model_response.model = model

        if mock_tool_calls:
            model_response.choices[0].message.tool_calls = [  # type: ignore
                ChatCompletionMessageToolCall(**tool_call)
                for tool_call in mock_tool_calls
            ]

        setattr(
            model_response,
            "usage",
            Usage(
                prompt_tokens=DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT,
                completion_tokens=DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT,
                total_tokens=DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT
                + DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT,
            ),
        )

        try:
            _, custom_llm_provider, _, _ = litellm.utils.get_llm_provider(model=model)
            model_response._hidden_params["custom_llm_provider"] = custom_llm_provider
        except Exception:
            # dont let setting a hidden param block a mock_respose
            pass

        if logging is not None:
            logging.post_call(
                input=messages,
                api_key="my-secret-key",
                original_response="my-original-response",
            )

        return model_response

    except Exception as e:
        if isinstance(e, openai.APIError):
            raise e
        raise Exception("Mock completion response failed - {}".format(e))

