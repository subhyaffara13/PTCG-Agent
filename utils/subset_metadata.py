
def subset_metadata(metadata, keep_only=None, exclude=None, unsupported_keys=None, remove=False):
    """Filter the metadata"""
    supported_keys = suppress_unsupported_keys(metadata, unsupported_keys=unsupported_keys)
    if keep_only is not None:
        include = [key for key in supported_keys if key in keep_only]
        filtered_metadata = {key: metadata[key] for key in include}
        sub_keep_only = second_level(keep_only)
        keys = [key for key in supported_keys if key in sub_keep_only]
        for key in keys:
            filtered_metadata[key] = subset_metadata(
                metadata[key],
                keep_only=sub_keep_only[key],
                unsupported_keys=unsupported_keys,
                remove=remove,
            )
    else:
        include = supported_keys
        filtered_metadata = {key: metadata[key] for key in supported_keys}

    if exclude is not None:
        for key in exclude:
            if key in filtered_metadata:
                filtered_metadata.pop(key)
        sub_exclude = second_level(exclude)
        for key in sub_exclude:
            if key in filtered_metadata:
                filtered_metadata[key] = subset_metadata(
                    filtered_metadata[key],
                    exclude=sub_exclude[key],
                    unsupported_keys=unsupported_keys,
                    remove=remove,
                )

    if remove:
        for key in set(include).difference(exclude or {}):
            metadata.pop(key, None)

    return filtered_metadata

