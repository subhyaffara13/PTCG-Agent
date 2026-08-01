
def image_edit(
    image: Optional[Union[FileTypes, List[FileTypes]]] = None,
    prompt: Optional[str] = None,
    model: Optional[str] = None,
    mask: Optional[str] = None,
    n: Optional[int] = None,
    quality: Optional[Union[str, ImageGenerationRequestQuality]] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    user: Optional[str] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[ImageResponse, Coroutine[Any, Any, ImageResponse]]:
    """
    Maps the image edit functionality, similar to OpenAI's images/edits endpoint.
    """
    local_vars = locals()
    try:
        openai_params = [
            "user",
            "request_timeout",
            "api_base",
            "api_version",
            "api_key",
            "deployment_id",
            "organization",
            "base_url",
            "default_headers",
            "timeout",
            "max_retries",
            "n",
            "quality",
            "size",
            "style",
            "async_call",
        ]
        litellm_params_list = all_litellm_params
        default_params = openai_params + litellm_params_list
        non_default_params = {
            k: v for k, v in kwargs.items() if k not in default_params
        }  # model-specific params - pass them straight to the model/provider
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        model_info = kwargs.get("model_info", None)
        metadata = kwargs.get("metadata", {})
        _is_async = kwargs.pop("async_call", False) is True

        # add images / or return a single image
        images = (
            image if isinstance(image, list) else ([image] if image is not None else [])
        )

        headers_from_kwargs = kwargs.get("headers")
        merged_extra_headers: Dict[str, Any] = {}
        if isinstance(headers_from_kwargs, dict):
            merged_extra_headers.update(headers_from_kwargs)
        if isinstance(extra_headers, dict):
            merged_extra_headers.update(extra_headers)

        if merged_extra_headers:
            extra_headers = dict(merged_extra_headers)

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)
        model, custom_llm_provider, _, _ = get_llm_provider(
            model=model or DEFAULT_IMAGE_ENDPOINT_MODEL,
            custom_llm_provider=custom_llm_provider,
        )

        # Check for custom provider
        if custom_llm_provider in litellm._custom_providers:
            custom_handler: Optional[CustomLLM] = None
            for item in litellm.custom_provider_map:
                if item["provider"] == custom_llm_provider:
                    custom_handler = item["custom_handler"]

            if custom_handler is None:
                raise LiteLLMUnknownProvider(
                    model=model, custom_llm_provider=custom_llm_provider
                )

            model_response = ImageResponse()

            if _is_async:
                async_custom_client: Optional[AsyncHTTPHandler] = None
                if kwargs.get("client") is not None and isinstance(
                    kwargs.get("client"), AsyncHTTPHandler
                ):
                    async_custom_client = kwargs.get("client")

                return custom_handler.aimage_edit(
                    model=model,
                    image=images,
                    prompt=prompt,
                    model_response=model_response,
                    api_key=kwargs.get("api_key"),
                    api_base=kwargs.get("api_base"),
                    optional_params=kwargs,
                    logging_obj=litellm_logging_obj,
                    timeout=timeout,
                    client=async_custom_client,
                )
            else:
                custom_client: Optional[HTTPHandler] = None
                if kwargs.get("client") is not None and isinstance(
                    kwargs.get("client"), HTTPHandler
                ):
                    custom_client = kwargs.get("client")

                return custom_handler.image_edit(
                    model=model,
                    image=images,
                    prompt=prompt,
                    model_response=model_response,
                    api_key=kwargs.get("api_key"),
                    api_base=kwargs.get("api_base"),
                    optional_params=kwargs,
                    logging_obj=litellm_logging_obj,
                    timeout=timeout,
                    client=custom_client,
                )

        # get provider config
        image_edit_provider_config: Optional[BaseImageEditConfig] = (
            ProviderConfigManager.get_provider_image_edit_config(
                model=model,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if image_edit_provider_config is None:
            raise ValueError(f"image edit is not supported for {custom_llm_provider}")

        local_vars.update(kwargs)
        # Get ImageEditOptionalRequestParams with only valid parameters
        image_edit_optional_params: (
            ImageEditOptionalRequestParams
        ) = _get_ImageEditRequestUtils().get_requested_image_edit_optional_param(
            local_vars
        )
        # Get optional parameters for the responses API
        image_edit_request_params: (
            Dict
        ) = _get_ImageEditRequestUtils().get_optional_params_image_edit(
            model=model,
            image_edit_provider_config=image_edit_provider_config,
            image_edit_optional_params=image_edit_optional_params,
            drop_params=kwargs.get("drop_params"),
            additional_drop_params=kwargs.get("additional_drop_params"),
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            user=user,
            optional_params=dict(image_edit_request_params),
            litellm_params={
                **image_edit_request_params,
                "litellm_call_id": litellm_call_id,
                "model_info": model_info,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Route bedrock to its specific handler (AWS signing required)
        if custom_llm_provider == "bedrock":
            if model is None:
                raise Exception("Model needs to be set for bedrock")
            image_edit_request_params.update(non_default_params)
            return bedrock_image_edit.image_edit(  # type: ignore
                model=model,
                image=images,
                prompt=prompt,
                timeout=timeout,
                logging_obj=litellm_logging_obj,
                optional_params=image_edit_request_params,
                model_response=ImageResponse(),
                aimage_edit=_is_async,
                client=kwargs.get("client"),
                api_base=kwargs.get("api_base"),
                extra_headers=extra_headers,
                api_key=kwargs.get("api_key"),
            )
        elif custom_llm_provider == "stability":
            image_edit_request_params.update(non_default_params)
            return base_llm_http_handler.image_edit_handler(
                model=model,
                image=images,
                prompt=prompt,
                image_edit_provider_config=image_edit_provider_config,
                image_edit_optional_request_params=image_edit_request_params,
                custom_llm_provider=custom_llm_provider,
                litellm_params=litellm_params,
                logging_obj=litellm_logging_obj,
                extra_headers=extra_headers,
                extra_body=extra_body,
                timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
                _is_async=_is_async,
                client=kwargs.get("client"),
            )
        elif custom_llm_provider == "black_forest_labs":
            # Route to BFL-specific handler (polling required)
            if model is None:
                raise Exception("Model needs to be set for black_forest_labs")
            image_edit_request_params.update(non_default_params)
            return bfl_image_edit.image_edit(
                model=model,
                image=images,
                prompt=prompt,
                image_edit_optional_request_params=image_edit_request_params,
                litellm_params=litellm_params,
                logging_obj=litellm_logging_obj,
                timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
                extra_headers=extra_headers,
                client=kwargs.get("client"),
                aimage_edit=_is_async,
            )
        # Call the handler with _is_async flag instead of directly calling the async handler
        return base_llm_http_handler.image_edit_handler(
            model=model,
            image=images,
            prompt=prompt,
            image_edit_provider_config=image_edit_provider_config,
            image_edit_optional_request_params=image_edit_request_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
            client=kwargs.get("client"),
        )

    except Exception as e:
        raise litellm.exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

