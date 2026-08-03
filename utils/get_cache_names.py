import os

def get_cache_names(id: str, path: str, options: Options) -> tuple[str, str, str | None]:
    """Return the file names for the cache files.

    Args:
      id: module ID
      path: module path
      options: build options

    Returns:
      A tuple with the file names to be used for the meta file, the
      data file, and the fine-grained deps JSON, respectively.
    """
    if options.cache_map:
        pair = options.cache_map.get(normpath(path, options))
    else:
        pair = None
    if pair is not None:
        # The cache map paths were specified relative to the base directory,
        # but the filesystem metastore APIs operates relative to the cache
        # prefix directory.
        # Solve this by rewriting the paths as relative to the root dir.
        # This only makes sense when using the filesystem backed cache.
        root = _cache_dir_prefix(options)
        return os.path.relpath(pair[0], root), os.path.relpath(pair[1], root), None
    prefix = os.path.join(*id.split("."))
    is_package = os.path.basename(path).startswith("__init__.py")
    if is_package:
        prefix = os_path_join(prefix, "__init__")

    deps_json = None
    if options.cache_fine_grained:
        deps_json = prefix + ".deps.json"
    if options.fixed_format_cache:
        data_suffix = ".data.ff"
        meta_suffix = ".meta.ff"
    else:
        data_suffix = ".data.json"
        meta_suffix = ".meta.json"
    return prefix + meta_suffix, prefix + data_suffix, deps_json

