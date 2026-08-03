import os
from typing import Any, Dict, Optional, Union

def list(
    github,
    force_reload=False,
    skip_validation=False,
    trust_repo="check",
    verbose=True,
):
    r"""
    List all callable entrypoints available in the repo specified by ``github``.

    Args:
        github (str): a string with format "repo_owner/repo_name[:ref]" with an optional
            ref (tag or branch). If ``ref`` is not specified, the default branch is assumed to be ``main`` if
            it exists, and otherwise ``master``.
            Example: 'pytorch/vision:0.10'
        force_reload (bool, optional): whether to discard the existing cache and force a fresh download.
            Default is ``False``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the branch or commit
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
        trust_repo (bool or str): ``"check"``, ``True`` or ``False``.
            This parameter was introduced in v1.12 and helps ensuring that users
            only run code from repos that they trust.

            - If ``False``, a prompt will ask the user whether the repo should
              be trusted.
            - If ``True``, the repo will be added to the trusted list and loaded
              without requiring explicit confirmation.
            - If ``"check"``, the repo will be checked against the list of
              trusted repos in the cache. If it is not present in that list, the
              behaviour will fall back onto the ``trust_repo=False`` option.

            Default is ``"check"``.
        verbose (bool, optional): If ``False``, mute messages about hitting
            local caches. Note that the message about first download cannot be
            muted. Default is ``True``.

    Returns:
        list: The available callables entrypoint

    Example:
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_HUB)
        >>> entrypoints = torch.hub.list("pytorch/vision", force_reload=True)
    """
    repo_dir = _get_cache_or_reload(
        github,
        force_reload,
        trust_repo,
        verbose=verbose,
        skip_validation=skip_validation,
    )

    with _add_to_sys_path(repo_dir):
        hubconf_path = os.path.join(repo_dir, MODULE_HUBCONF)
        hub_module = _import_module(MODULE_HUBCONF, hubconf_path)

    # We take functions starts with '_' as internal helper functions
    entrypoints = [
        f
        for f in dir(hub_module)
        if callable(getattr(hub_module, f)) and not f.startswith("_")
    ]

    return entrypoints


def list(
    after: Optional[str] = None,
    before: Optional[str] = None,
    limit: Optional[int] = 20,
    order: Optional[str] = "desc",
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
):
    """
    List vector stores.

    Args:
        after: A cursor for use in pagination.
        before: A cursor for use in pagination.
        limit: A limit on the number of objects to be returned.
        order: Sort order by the created_at timestamp.

    Returns:
        List of vector stores.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("alist", False) is True

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
                f"Vector store list is not supported for {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "after": after,
                "before": before,
                "limit": limit,
                "order": order,
            },
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_list_handler(
            after=after,
            before=before,
            limit=limit,
            order=order,
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


def list(
    *,
    vector_store_id: str,
    after: Optional[str] = None,
    before: Optional[str] = None,
    filter: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[
    VectorStoreFileListResponse, Coroutine[Any, Any, VectorStoreFileListResponse]
]:
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("alist", False) is True

        custom_llm_provider = _ensure_provider(custom_llm_provider)

        _prepare_registry_credentials(vector_store_id=vector_store_id, kwargs=kwargs)

        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
            provider=LlmProviders(custom_llm_provider)
        )
        if provider_config is None:
            raise ValueError(
                f"Vector store file list is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        list_query: VectorStoreFileListQueryParams = (
            VectorStoreFileRequestUtils.get_list_query_params(local_vars)
        )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"vector_store_id": vector_store_id, **list_query},
            litellm_params={
                "vector_store_id": vector_store_id,
                "litellm_call_id": litellm_call_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_file_list_handler(
            vector_store_id=vector_store_id,
            query_params=list_query,
            vector_store_files_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_query=extra_query,
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


def list(ctx: click.Context, output_format: Literal["table", "json"]):
    """List all credentials"""
    client = CredentialsManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    response = client.list()
    assert isinstance(response, dict)

    if output_format == "json":
        rich.print_json(data=response)
    else:  # table format
        table = Table(title="Credentials")

        # Add columns
        table.add_column("Credential Name", style="cyan")
        table.add_column("Custom LLM Provider", style="green")

        # Add rows
        for cred in response.get("credentials", []):
            info = cred.get("credential_info", {})
            table.add_row(
                str(cred.get("credential_name", "")),
                str(info.get("custom_llm_provider", "")),
            )

        rich.print(table)


def list(
    ctx: click.Context,
    page: Optional[int],
    size: Optional[int],
    user_id: Optional[str],
    team_id: Optional[str],
    organization_id: Optional[str],
    key_hash: Optional[str],
    key_alias: Optional[str],
    include_team_keys: bool,
    output_format: Literal["table", "json"],
    return_full_object: bool,
):
    """List all API keys"""
    client = KeysManagementClient(ctx.obj["base_url"], ctx.obj["api_key"])
    response = client.list(
        page=page,
        size=size,
        user_id=user_id,
        team_id=team_id,
        organization_id=organization_id,
        key_hash=key_hash,
        key_alias=key_alias,
        return_full_object=return_full_object,
        include_team_keys=include_team_keys,
    )
    assert isinstance(response, dict)

    if output_format == "json":
        rich.print_json(data=response)
    else:
        rich.print(
            f"Showing {len(response.get('keys', []))} keys out of {response.get('total_count', 0)}"
        )
        table = Table(title="API Keys")
        table.add_column("Key Hash", style="cyan")
        table.add_column("Alias", style="green")
        table.add_column("User ID", style="magenta")
        table.add_column("Team ID", style="yellow")
        table.add_column("Spend", style="red")
        for key in response.get("keys", []):
            table.add_row(
                str(key.get("token", "")),
                str(key.get("key_alias", "")),
                str(key.get("user_id", "")),
                str(key.get("team_id", "")),
                str(key.get("spend", "")),
            )
        rich.print(table)


def list(ctx: click.Context):
    """List teams that you belong to"""
    client = Client(ctx.obj["base_url"], ctx.obj["api_key"])

    try:
        # Use list() for simpler response structure (returns array directly)
        teams = client.teams.list()
        display_teams_table(teams)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {e.response.status_code}", err=True)
        error_body = e.response.json()
        click.echo(f"Details: {error_body.get('detail', 'Unknown error')}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


def list(
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[AgentListResponse, Coroutine[Any, Any, AgentListResponse]]:
    """Sync: List all agents on the provider side."""
    local_vars = locals()
    custom_llm_provider = (
        custom_llm_provider or kwargs.get("custom_llm_provider") or "gemini"
    )
    try:
        _is_async = kwargs.pop("alist_agents", False) is True
        kwargs.setdefault("custom_llm_provider", custom_llm_provider)
        litellm_params = GenericLiteLLMParams(**kwargs)
        logging_obj = _make_logging_obj(
            kwargs, "", custom_llm_provider, "list_agents", {}
        )
        config = _get_agents_api_config(custom_llm_provider)
        return agents_http_handler.list_agents(
            agents_api_config=config,
            litellm_params=litellm_params,
            logging_obj=logging_obj,
            extra_headers=extra_headers,
            timeout=timeout,
            _is_async=_is_async,
        )
    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

