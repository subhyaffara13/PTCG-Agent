from typing import Any, Dict, Optional, Set, Union

def _prepare_mcp_server_data(
    data: Union[NewMCPServerRequest, UpdateMCPServerRequest],
    exclude_unset: bool = False,
    fields_set: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    Helper function to prepare MCP server data for database operations.
    Handles JSON field serialization for mcp_info and env fields.

    Args:
        data: NewMCPServerRequest or UpdateMCPServerRequest object
        exclude_unset: When True, only fields the caller explicitly provided are
            included. Used for partial updates (PUT /v1/mcp/server) so omitted
            fields keep their existing DB value instead of being silently reset
            to a Pydantic schema default. ``exclude_none`` is not enough here:
            non-Optional fields (e.g. ``transport=MCPTransport.sse``,
            ``mcp_access_groups=[]``, ``allow_all_keys=False``) are backfilled
            with their default when omitted, and a non-None default survives the
            ``exclude_none`` filter and overwrites the row.

    Returns:
        Dict with properly serialized JSON fields
    """
    from litellm.litellm_core_utils.safe_json_dumps import safe_dumps

    # Convert model to dict.
    # - Partial update (exclude_unset): only caller-provided keys are emitted, so
    #   omitted fields are never written and keep their existing DB value.
    # - Create (exclude_none): drop None-valued fields and let DB defaults apply.
    if exclude_unset:
        if fields_set is None:
            fields_set = data.fields_set()
        data_dict = data.model_dump(exclude_unset=True)
        # ``validate_and_normalize_mcp_server_payload`` always assigns ``alias``
        # on the payload, which marks it as set even when the caller omitted it.
        # Drop it only when the original request omitted alias; an explicit
        # ``alias=None`` is a valid request to clear the stored alias.
        if data_dict.get("alias") is None and "alias" not in fields_set:
            data_dict.pop("alias", None)
        # Prisma ``allowed_tools`` is a required String[]; ``null`` is invalid.
        # The UI sends null to clear a whitelist — treat that as ``[]``.
        if "allowed_tools" in data_dict and data_dict["allowed_tools"] is None:
            data_dict["allowed_tools"] = []
        # Json map fields use ``@default("{}")``; explicit null means clear overrides.
        for json_map_field in (
            "tool_name_to_display_name",
            "tool_name_to_description",
        ):
            if json_map_field in data_dict and data_dict[json_map_field] is None:
                data_dict[json_map_field] = {}
    else:
        data_dict = data.model_dump(exclude_none=True)
        # Ensure alias is always present in the dict (even if None)
        if "alias" not in data_dict:
            data_dict["alias"] = getattr(data, "alias", None)

    # Handle credentials serialization
    credentials = data_dict.get("credentials")
    if credentials is not None:
        data_dict["credentials"] = encrypt_credentials(
            credentials=credentials, encryption_key=_get_salt_key()
        )
        data_dict["credentials"] = safe_dumps(data_dict["credentials"])

    # Serialize JSON fields from ``data_dict`` (not ``data``) so the
    # exclude_unset filter is respected. Reading back from ``data`` would
    # reintroduce defaults (e.g. ``env={}``) for fields the caller never set.
    if data_dict.get("static_headers") is not None:
        data_dict["static_headers"] = safe_dumps(data_dict["static_headers"])

    # env_vars is read from ``data_dict`` (not ``data``) like every other JSON
    # column so the exclude_unset filter is respected: a partial update that
    # omits env_vars never overwrites the stored value. Global values are
    # encrypted at rest before serialization.
    env_vars = data_dict.get("env_vars")
    if env_vars is not None:
        serialized_env_vars = [dict(v) for v in env_vars]
        _encrypt_global_env_var_values(serialized_env_vars)
        data_dict["env_vars"] = safe_dumps(serialized_env_vars)

    if data_dict.get("mcp_info") is not None:
        data_dict["mcp_info"] = safe_dumps(data_dict["mcp_info"])

    if data_dict.get("env") is not None:
        data_dict["env"] = safe_dumps(data_dict["env"])

    if "tool_name_to_display_name" in data_dict:
        data_dict["tool_name_to_display_name"] = safe_dumps(
            data_dict["tool_name_to_display_name"] or {}
        )
    if "tool_name_to_description" in data_dict:
        data_dict["tool_name_to_description"] = safe_dumps(
            data_dict["tool_name_to_description"] or {}
        )

    # mcp_access_groups is already List[str], no serialization needed

    # On create, force is_byok so a False value is always written to the DB. On
    # partial update, only write it when the caller explicitly provided it.
    if not exclude_unset:
        data_dict["is_byok"] = getattr(data, "is_byok", False)

    return data_dict

