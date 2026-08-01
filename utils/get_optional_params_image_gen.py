
def get_optional_params_image_gen(
    model: Optional[str] = None,
    n: Optional[int] = None,
    quality: Optional[str] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    user: Optional[str] = None,
    imageConfig: Optional[dict] = None,
    custom_llm_provider: Optional[str] = None,
    additional_drop_params: Optional[list] = None,
    provider_config: Optional[BaseImageGenerationConfig] = None,
    drop_params: Optional[bool] = None,
    **kwargs,
):
    # retrieve all parameters passed to the function
    passed_params = locals()
    model = passed_params.pop("model", None)
    custom_llm_provider = passed_params.pop("custom_llm_provider")
    provider_config = passed_params.pop("provider_config", None)
    drop_params = passed_params.pop("drop_params", None)
    additional_drop_params = passed_params.pop("additional_drop_params", None)
    special_params = passed_params.pop("kwargs")
    for k, v in special_params.items():
        if k.startswith("aws_") and (
            custom_llm_provider != "bedrock" and custom_llm_provider != "sagemaker"
        ):  # allow dynamically setting boto3 init logic
            continue
        elif k == "hf_model_name" and custom_llm_provider != "sagemaker":
            continue
        elif (
            k.startswith("vertex_")
            and custom_llm_provider != "vertex_ai"
            and custom_llm_provider != "vertex_ai_beta"
        ):  # allow dynamically setting vertex ai init logic
            continue
        passed_params[k] = v

    default_params = {
        "n": None,
        "quality": None,
        "response_format": None,
        "size": None,
        "style": None,
        "user": None,
        "imageConfig": None,
        "tools": None,
        "web_search_options": None,
    }

    non_default_params = _get_non_default_params(
        passed_params=passed_params,
        default_params=default_params,
        additional_drop_params=additional_drop_params,
    )
    optional_params: Dict[str, Any] = {}

    ## raise exception if non-default value passed for non-openai/azure embedding calls
    def _check_valid_arg(supported_params):
        if len(non_default_params.keys()) > 0:
            keys = list(non_default_params.keys())
            for k in keys:
                if (
                    litellm.drop_params is True or drop_params is True
                ) and k not in supported_params:  # drop the unsupported non-default values
                    non_default_params.pop(k, None)
                    passed_params.pop(k, None)
                elif k not in supported_params:
                    raise UnsupportedParamsError(
                        status_code=500,
                        message=f"Setting `{k}` is not supported by {custom_llm_provider}, {model}. To drop it from the call, set `litellm.drop_params = True`.",
                    )
            return non_default_params

    if provider_config is not None:
        supported_params = provider_config.get_supported_openai_params(
            model=model or ""
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = provider_config.map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model or "",
            drop_params=drop_params if drop_params is not None else False,
        )
    elif (
        custom_llm_provider == "openai"
        or custom_llm_provider == "azure"
        or custom_llm_provider in litellm.openai_compatible_providers
    ):
        optional_params = non_default_params
    elif custom_llm_provider == "bedrock":
        config_class = litellm.BedrockImageGeneration.get_config_class(model=model)
        supported_params = config_class.get_supported_openai_params(model=model)
        _check_valid_arg(supported_params=supported_params)
        optional_params = config_class.map_openai_params(
            non_default_params=non_default_params, optional_params={}
        )
    elif custom_llm_provider == "vertex_ai":
        supported_params = ["n", "size"]
        """
        All params here: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/imagegeneration?project=adroit-crow-413218
        """
        _check_valid_arg(supported_params=supported_params)
        if n is not None:
            optional_params["sampleCount"] = int(n)

        # Map OpenAI size parameter to Vertex AI aspectRatio
        if size is not None:
            optional_params["aspectRatio"] = _map_openai_size_to_vertex_ai_aspect_ratio(
                size
            )

    openai_params: list[str] = list(default_params.keys())
    if provider_config is not None:
        supported_params = provider_config.get_supported_openai_params(
            model=model or ""
        )
        openai_params = list(supported_params)

    optional_params = add_provider_specific_params_to_optional_params(
        optional_params=optional_params,
        passed_params=passed_params,
        custom_llm_provider=custom_llm_provider or "",
        openai_params=openai_params,
        additional_drop_params=additional_drop_params,
    )
    # remove keys with None or empty dict/list values to avoid sending empty payloads
    optional_params = {
        k: v
        for k, v in optional_params.items()
        if v is not None and (not isinstance(v, (dict, list)) or len(v) > 0)
    }
    return optional_params


def get_optional_params_image_gen(
    n: Optional[int] = None,
    quality: Optional[str] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    user: Optional[str] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
):
    # retrieve all parameters passed to the function
    passed_params = locals()
    custom_llm_provider = passed_params.pop("custom_llm_provider")
    special_params = passed_params.pop("kwargs")
    for k, v in special_params.items():
        passed_params[k] = v

    default_params = {
        "n": None,
        "quality": None,
        "response_format": None,
        "size": None,
        "style": None,
        "user": None,
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
                    raise UnsupportedParamsError(
                        status_code=500,
                        message=f"Setting user/encoding format is not supported by {custom_llm_provider}. To drop it from the call, set `litellm.drop_params = True`.",
                    )
            return non_default_params

    if (
        custom_llm_provider == "openai"
        or custom_llm_provider == "azure"
        or custom_llm_provider in litellm.openai_compatible_providers
    ):
        optional_params = non_default_params
    elif custom_llm_provider == "bedrock":
        supported_params = ["size"]
        _check_valid_arg(supported_params=supported_params)
        if size is not None:
            width, height = size.split("x")
            optional_params["width"] = int(width)
            optional_params["height"] = int(height)
    elif custom_llm_provider == "vertex_ai":
        supported_params = ["n"]
        """
        All params here: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/imagegeneration?project=adroit-crow-413218
        """
        _check_valid_arg(supported_params=supported_params)
        if n is not None:
            optional_params["sampleCount"] = int(n)

    for k in passed_params.keys():
        if k not in default_params.keys():
            optional_params[k] = passed_params[k]
    return optional_params

