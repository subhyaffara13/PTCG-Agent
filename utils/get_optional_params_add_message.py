
def get_optional_params_add_message(
    role: Optional[str],
    content: Optional[
        Union[
            str,
            List[
                Union[
                    MessageContentTextObject,
                    MessageContentImageFileObject,
                    MessageContentImageURLObject,
                ]
            ],
        ]
    ],
    attachments: Optional[List[Attachment]],
    metadata: Optional[dict],
    custom_llm_provider: str,
    **kwargs,
):
    """
    Azure doesn't support 'attachments' for creating a message

    Reference - https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference-messages?tabs=python#create-message
    """
    passed_params = locals()
    custom_llm_provider = passed_params.pop("custom_llm_provider")
    special_params = passed_params.pop("kwargs")
    for k, v in special_params.items():
        passed_params[k] = v

    default_params = {
        "role": None,
        "content": None,
        "attachments": None,
        "metadata": None,
    }

    non_default_params = {
        k: v
        for k, v in passed_params.items()
        if (k in default_params and v != default_params[k])
    }
    optional_params = {}

    ## raise exception if non-default value passed for non-openai/azure embedding calls
    def _check_valid_arg(supported_params):
        if len(non_default_params.keys()) > 0:
            keys = list(non_default_params.keys())
            for k in keys:
                if (
                    litellm.drop_params is True and k not in supported_params
                ):  # drop the unsupported non-default values
                    non_default_params.pop(k, None)
                elif k not in supported_params:
                    raise litellm.utils.UnsupportedParamsError(
                        status_code=500,
                        message="k={}, not supported by {}. Supported params={}. To drop it from the call, set `litellm.drop_params = True`.".format(
                            k, custom_llm_provider, supported_params
                        ),
                    )
            return non_default_params

    if custom_llm_provider == "openai":
        optional_params = non_default_params
    elif custom_llm_provider == "azure":
        supported_params = (
            litellm.AzureOpenAIAssistantsAPIConfig().get_supported_openai_create_message_params()
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.AzureOpenAIAssistantsAPIConfig().map_openai_params_create_message_params(
            non_default_params=non_default_params, optional_params=optional_params
        )
    for k in passed_params.keys():
        if k not in default_params.keys():
            optional_params[k] = passed_params[k]
    return optional_params

