
def _get_dcp_custom_metadata(metadata: Any) -> Any | None:
    if DEFAULT_EXTRA_METADATA_KEY in metadata:
        custom_metadata = metadata[DEFAULT_EXTRA_METADATA_KEY]
        if CUSTOM_METADATA_KEY in custom_metadata:
            return json.loads(custom_metadata[CUSTOM_METADATA_KEY])
    return None

