from typing import Dict, Optional

def moderation(
    input: str, model: Optional[str] = None, api_key: Optional[str] = None, **kwargs
) -> OpenAIModerationResponse:
    # only supports open ai for now
    api_key = (
        api_key
        or litellm.api_key
        or litellm.openai_key
        or get_secret_str("OPENAI_API_KEY")
    )

    # Extract api_base from kwargs
    api_base = kwargs.get("api_base", None)

    openai_client = kwargs.get("client", None)
    if openai_client is None:
        if api_base is not None:
            openai_client = openai.OpenAI(api_key=api_key, base_url=api_base)
        else:
            openai_client = openai.OpenAI(api_key=api_key)

    if model is not None:
        response = openai_client.moderations.create(input=input, model=model)
    else:
        response = openai_client.moderations.create(input=input)

    response_dict: Dict = response.model_dump()
    return litellm.utils.LiteLLMResponseObjectHandler.convert_to_moderation_response(
        response_object=response_dict,
    )

