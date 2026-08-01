
def suppress_unsupported_keys(metadata, unsupported_keys=None):
    # assert isinstance(unsupported_keys, set)
    if isinstance(unsupported_keys, set):
        for key in metadata:
            if not is_valid_metadata_key(key):
                unsupported_keys.add(key)
    return [key for key in metadata if is_valid_metadata_key(key)]

