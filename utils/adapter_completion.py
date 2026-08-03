from typing import Optional, Union

def adapter_completion(
    *, adapter_id: str, **kwargs
) -> Optional[Union[BaseModel, AdapterCompletionStreamWrapper]]:
    translation_obj: Optional[CustomLogger] = None
    for item in litellm.adapters:
        if item["id"] == adapter_id:
            translation_obj = item["adapter"]

    if translation_obj is None:
        raise ValueError(
            "No matching adapter given. Received 'adapter_id'={}, litellm.adapters={}".format(
                adapter_id, litellm.adapters
            )
        )

    new_kwargs = translation_obj.translate_completion_input_params(kwargs=kwargs)

    response: Union[ModelResponse, CustomStreamWrapper] = completion(**new_kwargs)  # type: ignore
    translated_response: Optional[Union[BaseModel, AdapterCompletionStreamWrapper]] = (
        None
    )
    if isinstance(response, ModelResponse):
        translated_response = translation_obj.translate_completion_output_params(
            response=response
        )
    elif isinstance(response, CustomStreamWrapper) or inspect.isgenerator(response):
        translated_response = (
            translation_obj.translate_completion_output_params_streaming(
                completion_stream=response
            )
        )

    return translated_response

