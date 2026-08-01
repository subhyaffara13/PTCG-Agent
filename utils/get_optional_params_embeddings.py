
def get_optional_params_embeddings(
    # 2 optional params
    model: str,
    user: Optional[str] = None,
    encoding_format: Optional[str] = None,
    dimensions: Optional[int] = None,
    custom_llm_provider="",
    drop_params: Optional[bool] = None,
    additional_drop_params: Optional[List[str]] = None,
    allowed_openai_params: Optional[List[str]] = None,
    **kwargs,
):
    # Lazy load get_supported_openai_params
    get_supported_openai_params = getattr(
        sys.modules[__name__], "get_supported_openai_params"
    )

    # retrieve all parameters passed to the function
    passed_params = locals()
    custom_llm_provider = passed_params.pop("custom_llm_provider", None)
    special_params = passed_params.pop("kwargs")

    drop_params = passed_params.pop("drop_params", None)
    additional_drop_params = passed_params.pop("additional_drop_params", None)
    allowed_openai_params = passed_params.pop("allowed_openai_params", None) or []
    # Remove function objects from passed_params to avoid JSON serialization errors
    passed_params.pop("get_supported_openai_params", None)

    def _check_valid_arg(supported_params: Optional[list]):
        if supported_params is None:
            return
        unsupported_params = {}
        for k in non_default_params.keys():
            if k not in supported_params:
                unsupported_params[k] = non_default_params[k]
        if unsupported_params:
            if litellm.drop_params is True or (
                drop_params is not None and drop_params is True
            ):
                pass
            else:
                raise UnsupportedParamsError(
                    status_code=500,
                    message=f"{custom_llm_provider} does not support parameters: {unsupported_params}, for model={model}. To drop these, set `litellm.drop_params=True` or for proxy:\n\n`litellm_settings:\n drop_params: true`\n",
                )

    non_default_params = (
        PreProcessNonDefaultParams.embedding_pre_process_non_default_params(
            passed_params=passed_params,
            special_params=special_params,
            custom_llm_provider=custom_llm_provider,
            additional_drop_params=additional_drop_params,
            model=model,
        )
    )

    provider_config: Optional[BaseEmbeddingConfig] = None

    optional_params = {}
    if (
        custom_llm_provider is not None
        and custom_llm_provider in LlmProviders._member_map_.values()
    ):
        provider_config = ProviderConfigManager.get_provider_embedding_config(
            model=model,
            provider=LlmProviders(custom_llm_provider),
        )

    if provider_config is not None:
        supported_params: Optional[list] = provider_config.get_supported_openai_params(
            model=model
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = provider_config.map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )
        # Provider-only params (e.g. Cohere input_type) are not in
        # OPENAI_EMBEDDING_PARAMS, so embedding_pre_process drops them from
        # non_default_params before map_openai_params. Restore only those extras
        # from passed_params — skip OPENAI_EMBEDDING_PARAMS to avoid duplicating
        # values already mapped (e.g. dimensions -> output_dimension).
        if supported_params:
            for param in supported_params:
                if param in OPENAI_EMBEDDING_PARAMS:
                    continue
                if (
                    param in passed_params
                    and passed_params[param] is not None
                    and param not in optional_params
                ):
                    optional_params[param] = passed_params[param]
    ## raise exception if non-default value passed for non-openai/azure embedding calls
    elif custom_llm_provider == "openai":
        # 'dimensions` is only supported in `text-embedding-3` and later models
        if (
            model is not None
            and "text-embedding-3" not in model
            and "dimensions" in non_default_params.keys()
            and "dimensions" not in (allowed_openai_params or [])
        ):
            # Honor drop_params (per-call) and litellm.drop_params (global) the same
            # way `_check_valid_arg` does above. The raised error message itself
            # tells users to set `drop_params=True`, so respect it here.
            if litellm.drop_params is True or drop_params is True:
                non_default_params.pop("dimensions", None)
            else:
                raise UnsupportedParamsError(
                    status_code=500,
                    message="Setting dimensions is not supported for OpenAI `text-embedding-3` and later models. To drop it from the call, set `litellm.drop_params = True`.",
                )
        optional_params = non_default_params
    elif custom_llm_provider == "triton":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider=custom_llm_provider,
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.TritonEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )
    elif custom_llm_provider == "databricks":
        supported_params = get_supported_openai_params(
            model=model or "",
            custom_llm_provider="databricks",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.DatabricksEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params, optional_params={}
        )

    elif custom_llm_provider == "nvidia_nim":
        supported_params = get_supported_openai_params(
            model=model or "",
            custom_llm_provider="nvidia_nim",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.nvidiaNimEmbeddingConfig.map_openai_params(
            non_default_params=non_default_params, optional_params={}, kwargs=kwargs
        )
    elif custom_llm_provider == "vertex_ai" or custom_llm_provider == "gemini":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="vertex_ai",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        (
            optional_params,
            kwargs,
        ) = litellm.VertexAITextEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params, optional_params={}, kwargs=kwargs
        )
    elif custom_llm_provider == "lm_studio":
        supported_params = (
            litellm.LmStudioEmbeddingConfig().get_supported_openai_params()
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.LmStudioEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params, optional_params={}
        )
    elif custom_llm_provider == "bedrock":
        # if dimensions is in non_default_params -> pass it for model=bedrock/amazon.titan-embed-text-v2
        if "amazon.titan-embed-text-v1" in model:
            object: Any = litellm.AmazonTitanG1Config()
        elif "amazon.titan-embed-image-v1" in model:
            object = litellm.AmazonTitanMultimodalEmbeddingG1Config()
        elif "amazon.titan-embed-text-v2:0" in model:
            object = litellm.AmazonTitanV2Config()
        elif "cohere.embed-multilingual-v3" in model or "cohere.embed-v4" in model:
            object = litellm.BedrockCohereEmbeddingConfig()
        elif "twelvelabs" in model or "marengo" in model:
            object = litellm.TwelveLabsMarengoEmbeddingConfig()
        elif "nova" in model.lower():
            object = litellm.AmazonNovaEmbeddingConfig()
        else:  # unmapped model
            supported_params = []
            _check_valid_arg(supported_params=supported_params)
            final_params = {**kwargs}
            return final_params

        supported_params = object.get_supported_openai_params()
        _check_valid_arg(supported_params=supported_params)
        optional_params = object.map_openai_params(
            non_default_params=non_default_params, optional_params={}
        )
    elif custom_llm_provider == "mistral":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="mistral",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.MistralEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params, optional_params={}
        )
    elif custom_llm_provider == "jina_ai":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="jina_ai",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.JinaAIEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )
    elif custom_llm_provider == "voyage":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="voyage",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        if litellm.VoyageContextualEmbeddingConfig.is_contextualized_embeddings(model):
            optional_params = (
                litellm.VoyageContextualEmbeddingConfig().map_openai_params(
                    non_default_params=non_default_params,
                    optional_params={},
                    model=model,
                    drop_params=drop_params if drop_params is not None else False,
                )
            )
        elif litellm.VoyageMultimodalEmbeddingConfig.is_multimodal_embeddings(model):
            optional_params = (
                litellm.VoyageMultimodalEmbeddingConfig().map_openai_params(
                    non_default_params=non_default_params,
                    optional_params={},
                    model=model,
                    drop_params=drop_params if drop_params is not None else False,
                )
            )
        else:
            optional_params = litellm.VoyageEmbeddingConfig().map_openai_params(
                non_default_params=non_default_params,
                optional_params={},
                model=model,
                drop_params=drop_params if drop_params is not None else False,
            )
        final_params = {**optional_params, **kwargs}
        return final_params
    elif custom_llm_provider == "sap":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="sap",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.GenAIHubEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )
    elif custom_llm_provider == "infinity":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="infinity",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.InfinityEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )

        final_params = {**optional_params, **kwargs}
        return final_params

    elif custom_llm_provider == "fireworks_ai":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="fireworks_ai",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.FireworksAIEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params, optional_params={}, model=model
        )
    elif custom_llm_provider == "sambanova":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="sambanova",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.SambaNovaEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )
    elif custom_llm_provider == "ovhcloud":
        supported_params = get_supported_openai_params(
            model=model,
            custom_llm_provider="ovhcloud",
            request_type="embeddings",
        )
        _check_valid_arg(supported_params=supported_params)
        optional_params = litellm.OVHCloudEmbeddingConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params={},
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )

    elif custom_llm_provider == "ollama":
        if "dimensions" in non_default_params:
            optional_params["dimensions"] = non_default_params.pop("dimensions")
        if len(non_default_params.keys()) > 0:
            if (
                litellm.drop_params is True or drop_params is True
            ):  # drop the unsupported non-default values
                keys = list(non_default_params.keys())
                for k in keys:
                    non_default_params.pop(k, None)
            else:
                raise UnsupportedParamsError(
                    status_code=500,
                    message=f"Setting {non_default_params} is not supported by {custom_llm_provider}. To drop it from the call, set `litellm.drop_params = True`.",
                )
    elif (
        custom_llm_provider != "openai"
        and custom_llm_provider != "azure"
        and custom_llm_provider not in litellm.openai_compatible_providers
    ):
        if len(non_default_params.keys()) > 0:
            if (
                litellm.drop_params is True or drop_params is True
            ):  # drop the unsupported non-default values
                keys = list(non_default_params.keys())
                for k in keys:
                    non_default_params.pop(k, None)
            else:
                raise UnsupportedParamsError(
                    status_code=500,
                    message=f"Setting {non_default_params} is not supported by {custom_llm_provider}. To drop it from the call, set `litellm.drop_params = True`.",
                )
        else:
            optional_params = non_default_params
    else:
        optional_params = non_default_params

    final_params = add_provider_specific_params_to_optional_params(
        optional_params=optional_params,
        passed_params=passed_params,
        custom_llm_provider=custom_llm_provider,
        openai_params=list(DEFAULT_EMBEDDING_PARAM_VALUES.keys()),
        additional_drop_params=kwargs.get("additional_drop_params", None),
    )

    if "extra_body" in final_params and len(final_params["extra_body"]) == 0:
        final_params.pop("extra_body", None)

    return final_params

