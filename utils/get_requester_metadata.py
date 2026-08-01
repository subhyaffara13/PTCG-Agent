
def get_requester_metadata(metadata: dict):
    if not metadata:
        return None

    requester_metadata = metadata.get("requester_metadata")
    if isinstance(requester_metadata, dict):
        cleaned_metadata = add_openai_metadata(requester_metadata)
        if cleaned_metadata:
            return cleaned_metadata

    cleaned_metadata = add_openai_metadata(metadata)
    if cleaned_metadata:
        return cleaned_metadata

    return None

