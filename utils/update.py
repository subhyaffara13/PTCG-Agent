from typing import Any, Dict, Optional, Union

def update(op, device_name, version, key, value):
    """Update the db of op parameters."""
    # skip storing possible optimization failures:
    if not value:
        warnings.warn(
            f"skipping empty value for {op}: {device_name=} {version=} {key=}",
            stacklevel=2,
        )
        return
    if (op, device_name, version) in _operation_device_version_data:
        if _operation_device_version_data[op, device_name, version].get(key) == value:
            return
        _operation_device_version_data[op, device_name, version][key] = value
    else:
        _operation_device_version_data[op, device_name, version] = {key: value}


def update(
    vector_store_id: str,
    name: Optional[str] = None,
    expires_after: Optional[Dict] = None,
    metadata: Optional[Dict[str, str]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreCreateResponse, Coroutine[Any, Any, VectorStoreCreateResponse]]:
    """
    Update a vector store.

    Args:
        vector_store_id: The ID of the vector store to update.
        name: The name of the vector store.
        expires_after: The expiration policy for the vector store.
        metadata: Set of 16 key-value pairs that can be attached to an object.

    Returns:
        VectorStoreCreateResponse containing the updated vector store details.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aupdate", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        if "/" in custom_llm_provider:
            api_type, custom_llm_provider, _, _ = get_llm_provider(
                model=custom_llm_provider,
                custom_llm_provider=None,
                litellm_params=None,
            )
        else:
            api_type = None
            custom_llm_provider = custom_llm_provider

        vector_store_provider_config = (
            ProviderConfigManager.get_provider_vector_stores_config(
                provider=litellm.LlmProviders(custom_llm_provider),
                api_type=api_type,
            )
        )

        if vector_store_provider_config is None:
            raise ValueError(
                f"Vector store update is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        vector_store_update_optional_params: VectorStoreCreateOptionalRequestParams = (
            VectorStoreRequestUtils.get_requested_vector_store_create_optional_param(
                local_vars
            )
        )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "vector_store_id": vector_store_id,
                "name": name,
                **vector_store_update_optional_params,
            },
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_update_handler(
            vector_store_id=vector_store_id,
            vector_store_update_optional_params=vector_store_update_optional_params,
            vector_store_provider_config=vector_store_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def update(
    *,
    vector_store_id: str,
    file_id: str,
    attributes: VectorStoreFileAttributes,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreFileObject, Coroutine[Any, Any, VectorStoreFileObject]]:
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("aupdate", False) is True

        custom_llm_provider = _ensure_provider(custom_llm_provider)

        _prepare_registry_credentials(vector_store_id=vector_store_id, kwargs=kwargs)

        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
            provider=LlmProviders(custom_llm_provider)
        )
        if provider_config is None:
            raise ValueError(
                f"Vector store file update is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        update_request: VectorStoreFileUpdateRequest = (
            VectorStoreFileRequestUtils.get_update_request_params(local_vars)
        )
        update_request["attributes"] = attributes

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "vector_store_id": vector_store_id,
                "file_id": file_id,
                **update_request,
            },
            litellm_params={
                "vector_store_id": vector_store_id,
                "litellm_call_id": litellm_call_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_file_update_handler(
            vector_store_id=vector_store_id,
            file_id=file_id,
            update_request=update_request,
            vector_store_files_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            client=kwargs.get("client"),
            _is_async=_is_async,
        )
        return response
    except Exception as e:  # noqa: BLE001
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def update(
    name: NameArg,
    namespace: NamespaceOpt = None,
    repo: Annotated[
        str | None,
        typer.Option(
            help="The name of the model repository associated with the Inference Endpoint (e.g. 'openai/gpt-oss-120b').",
        ),
    ] = None,
    accelerator: Annotated[
        str | None,
        typer.Option(
            help="The hardware accelerator to be used for inference (e.g. 'cpu').",
        ),
    ] = None,
    instance_size: Annotated[
        str | None,
        typer.Option(
            help="The size or type of the instance to be used for hosting the model (e.g. 'x4').",
        ),
    ] = None,
    instance_type: Annotated[
        str | None,
        typer.Option(
            help="The cloud instance type where the Inference Endpoint will be deployed (e.g. 'intel-icl').",
        ),
    ] = None,
    framework: Annotated[
        str | None,
        typer.Option(
            help="The machine learning framework used for the model (e.g. 'custom').",
        ),
    ] = None,
    revision: Annotated[
        str | None,
        typer.Option(
            help="The specific model revision to deploy on the Inference Endpoint (e.g. '6c0e6080953db56375760c0471a8c5f2929baf11').",
        ),
    ] = None,
    task: Annotated[
        str | None,
        typer.Option(
            help="The task on which to deploy the model (e.g. 'text-classification').",
        ),
    ] = None,
    min_replica: Annotated[
        int | None,
        typer.Option(
            help="The minimum number of replicas (instances) to keep running for the Inference Endpoint.",
        ),
    ] = None,
    max_replica: Annotated[
        int | None,
        typer.Option(
            help="The maximum number of replicas (instances) to scale to for the Inference Endpoint.",
        ),
    ] = None,
    scale_to_zero_timeout: Annotated[
        int | None,
        typer.Option(
            help="The duration in minutes before an inactive endpoint is scaled to zero.",
        ),
    ] = None,
    scaling_metric: Annotated[
        InferenceEndpointScalingMetric | None,
        typer.Option(
            help="The metric reference for scaling.",
        ),
    ] = None,
    scaling_threshold: Annotated[
        float | None,
        typer.Option(
            help="The scaling metric threshold used to trigger a scale up. Ignored when scaling metric is not provided.",
        ),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Update an existing endpoint."""
    api = get_hf_api(token=token)
    try:
        endpoint = api.update_inference_endpoint(
            name=name,
            namespace=namespace,
            repository=repo,
            framework=framework,
            revision=revision,
            task=task,
            accelerator=accelerator,
            instance_size=instance_size,
            instance_type=instance_type,
            min_replica=min_replica,
            max_replica=max_replica,
            scale_to_zero_timeout=scale_to_zero_timeout,
            scaling_metric=scaling_metric,
            scaling_threshold=scaling_threshold,
            token=token,
        )
    except HfHubHTTPError as error:
        out.error(f"Update failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error
    out.dict(endpoint.raw)


def update() -> None:
    """Update the `hf` CLI to the latest version."""
    out.text(f"Current version: {__version__}")
    out.text("Checking for updates to latest version...")
    latest_version = _fetch_latest_pypi_version("huggingface_hub")
    if latest_version is not None and __version__ == latest_version:
        out.text(f"hf is up to date ({__version__})")
        return

    returncode = run_update()
    if returncode != 0:
        raise typer.Exit(code=returncode)
    out.hint(
        "You may also want to run `hf skills update` to refresh any installed skills "
        "so your AI agent sees the latest command surface."
    )


def update(node, state: tp.Any, /, *states: tp.Any) -> None:
  """Update the given graph node with a new state(s) in-place.

  Example usage::

    >>> from flax import nnx
    >>> import jax, jax.numpy as jnp

    >>> x = jnp.ones((1, 2))
    >>> y = jnp.ones((1, 3))
    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))

    >>> def loss_fn(model, x, y):
    ...   return jnp.mean((y - model(x))**2)
    >>> prev_loss = loss_fn(model, x, y)

    >>> grads = nnx.grad(loss_fn)(model, x, y)
    >>> new_state = jax.tree.map(lambda p, g: p - 0.1*g, nnx.state(model), grads)
    >>> nnx.update(model, new_state)
    >>> assert loss_fn(model, x, y) < prev_loss

  Args:
    node: A graph node to update.
    state: A :class:`State` object.
    *states: Additional :class:`State` objects.
  """
  if states:
    if isinstance(node, Variable):
      non_empty_states = [
        _state
        for _state in (state, *states)
        if not isinstance(_state, tp.Mapping) or _state
      ]
      if len(non_empty_states) != 1:
        all_states = (state, *states)
        raise ValueError(
          f'Expected exactly one non-empty state, got: {all_states!r}'
        )
      state = non_empty_states[0]
    else:
      state = statelib.merge_state(state, *states)
  _graph_update_dynamic(node, state)

