
def _update_metadata_field(updated_kv: dict, field_name: str) -> None:
    """
    Helper function to update metadata fields that require premium user checks in the update endpoint

    Args:
        updated_kv: The key-value dict being used for the update
        field_name: Name of the metadata field being updated
    """
    if field_name in LiteLLM_ManagementEndpoint_MetadataFields_Premium:
        # The UI sends falsy defaults (False, [], {}) even when the user has not
        # enabled any enterprise feature (see #20304, #30285); require a license
        # only for a truthy value. The falsy value is still persisted below so a
        # previously-set field can be cleared.
        if updated_kv.get(field_name):
            _premium_user_check()

    if field_name in updated_kv and updated_kv[field_name] is not None:
        # remove field from updated_kv
        _value = updated_kv.pop(field_name)
        if "metadata" in updated_kv and updated_kv["metadata"] is not None:
            updated_kv["metadata"][field_name] = _value
        else:
            updated_kv["metadata"] = {field_name: _value}

