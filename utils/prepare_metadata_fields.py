
def prepare_metadata_fields(
    data: BaseModel, non_default_values: dict, existing_metadata: dict
) -> dict:
    """
    Check LiteLLM_ManagementEndpoint_MetadataFields (proxy/_types.py) for fields that are allowed to be updated
    """
    if "metadata" not in non_default_values:  # allow user to set metadata to none
        non_default_values["metadata"] = existing_metadata.copy()

    casted_metadata = cast(dict, non_default_values["metadata"])

    # Reserved metadata fields are immutable once set. Preserve the existing value
    # when omitted, reject any explicit attempt to change it (including null).
    for reserved_field in LiteLLM_Reserved_Metadata_Fields:
        existing_value = existing_metadata.get(reserved_field)
        if existing_value is None:
            continue
        if casted_metadata is None or (
            reserved_field in casted_metadata
            and casted_metadata[reserved_field] != existing_value
        ):
            raise HTTPException(
                status_code=400,
                detail=f"{reserved_field} is immutable once set and cannot be changed via update.",
            )
        casted_metadata[reserved_field] = existing_value

    data_json = data.model_dump(exclude_unset=True, exclude_none=True)

    try:
        for k, v in data_json.items():
            if k in LiteLLM_ManagementEndpoint_MetadataFields:
                if isinstance(v, datetime):
                    casted_metadata[k] = v.isoformat()
                else:
                    casted_metadata[k] = v
            if k in LiteLLM_ManagementEndpoint_MetadataFields_Premium:
                from litellm.proxy.utils import _premium_user_check

                if v:
                    _premium_user_check(k)
                casted_metadata[k] = v

    except Exception as e:
        verbose_proxy_logger.exception(
            "litellm.proxy.proxy_server.prepare_metadata_fields(): Exception occured - {}".format(
                str(e)
            )
        )

    non_default_values["metadata"] = encrypt_callback_vars(casted_metadata)
    return non_default_values

