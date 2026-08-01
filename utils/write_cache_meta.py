
def write_cache_meta(meta: CacheMeta, manager: BuildManager, meta_file: str) -> None:
    # Write meta cache file
    metastore = manager.metastore
    if manager.options.fixed_format_cache:
        data_io = WriteBuffer()
        meta.write(data_io)
        # Prefix with both low- and high-level cache format versions for future validation.
        # TODO: switch to something like librt.internal.write_byte() if this is slow.
        meta_bytes = bytes([cache_version(), CACHE_VERSION]) + data_io.getvalue()
    else:
        meta_dict = meta.serialize()
        meta_bytes = json_dumps(meta_dict, manager.options.debug_cache)
    if not metastore.write(meta_file, meta_bytes):
        # Most likely the error is the replace() call
        # (see https://github.com/python/mypy/issues/3215).
        # The next run will simply find the cache entry out of date.
        manager.log(f"Error writing cache meta file {meta_file}")

