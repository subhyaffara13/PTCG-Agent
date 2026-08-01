
def log_requester_metadata(clean_metadata: dict):
    returned_metadata = {}
    requester_metadata = clean_metadata.get("requester_metadata") or {}
    for k, v in clean_metadata.items():
        if k not in requester_metadata:
            returned_metadata[k] = v

    returned_metadata.update({"requester_metadata": requester_metadata})

    return returned_metadata

