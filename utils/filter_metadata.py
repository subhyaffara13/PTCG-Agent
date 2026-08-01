
def filter_metadata(metadata, user_filter, default_filter="", unsupported_keys=None, **kwargs):
    """Filter the cell or notebook metadata, according to the user preference"""
    default_filter = metadata_filter_as_dict(default_filter) or {}
    user_filter = metadata_filter_as_dict(user_filter) or {}

    default_exclude = default_filter.get("excluded", [])
    default_include = default_filter.get("additional", [])

    assert not (default_exclude == "all" and default_include == "all")
    if isinstance(default_include, list) and default_include and default_exclude == []:
        default_exclude = "all"

    user_exclude = user_filter.get("excluded", [])
    user_include = user_filter.get("additional", [])

    # notebook default filter = include only few metadata
    if default_exclude == "all":
        if user_include == "all":
            return subset_metadata(
                metadata,
                exclude=user_exclude,
                unsupported_keys=unsupported_keys,
                **kwargs,
            )
        if user_exclude == "all":
            return subset_metadata(
                metadata,
                keep_only=user_include,
                unsupported_keys=unsupported_keys,
                **kwargs,
            )
        return subset_metadata(
            metadata,
            keep_only=set(user_include).union(default_include),
            exclude=user_exclude,
            unsupported_keys=unsupported_keys,
            **kwargs,
        )

    # cell default filter = all metadata but removed ones
    if user_include == "all":
        return subset_metadata(
            metadata,
            exclude=user_exclude,
            unsupported_keys=unsupported_keys,
            **kwargs,
        )
    if user_exclude == "all":
        return subset_metadata(
            metadata,
            keep_only=user_include,
            unsupported_keys=unsupported_keys,
            **kwargs,
        )
    # Do not serialize empty tags
    if "tags" in metadata and not metadata["tags"]:
        metadata = metadata.copy()
        metadata.pop("tags")
    return subset_metadata(
        metadata,
        exclude=set(user_exclude).union(set(default_exclude).difference(user_include)),
        unsupported_keys=unsupported_keys,
        **kwargs,
    )

