
def base_path_and_adjusted_fmt(path: str, fmt: dict[str, str]) -> tuple[str, dict[str, str]]:
    """Return the base path and possibly adjusted Jupytext format
    that matches the current path"""
    assert isinstance(fmt, dict), "fmt must be a dictionary"
    fmt = dict(fmt)  # make a copy
    prefix = fmt.get("prefix", "")
    (
        prefix_root,
        prefix_dir,
        prefix_file_name,
    ) = get_prefix_root_prefix_dir_prefix_file_name(prefix)

    try:
        return base_path(path, fmt), fmt
    except InconsistentSuffix:
        del fmt["suffix"]
        return base_path(path, fmt), fmt
    except InconsistentPrefixRoot:
        if not prefix_root:
            raise
        fmt["prefix"] = get_prefix("", prefix_dir, prefix_file_name)
        if not fmt["prefix"]:
            del fmt["prefix"]
        return base_path(path, fmt), fmt
    except InconsistentPrefix:
        if not prefix_file_name:
            raise
        fmt["prefix"] = get_prefix(prefix_root, prefix_dir, "")
        if not fmt["prefix"]:
            del fmt["prefix"]
        return base_path(path, fmt), fmt
    except InconsistentPrefixDirectory:
        if not prefix_dir:
            raise
        fmt["prefix"] = get_prefix(prefix_root, "", prefix_file_name)
        if not fmt["prefix"]:
            del fmt["prefix"]
        return base_path(path, fmt), fmt

