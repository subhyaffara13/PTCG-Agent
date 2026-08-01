
def write_cache_meta_ex(meta_file: str, meta_ex: CacheMetaEx, manager: BuildManager) -> None:
    # Write errors cache file
    meta_ex_file = get_meta_ex_name(meta_file)
    metastore = manager.metastore
    if manager.options.fixed_format_cache:
        data_io = WriteBuffer()
        meta_ex.write(data_io)
        meta_bytes = data_io.getvalue()
    else:
        # Some generic JSON helpers require top-level to be a dict.
        meta_bytes = json_dumps(meta_ex.serialize(), manager.options.debug_cache)
    if not metastore.write(meta_ex_file, meta_bytes):
        manager.log(f"Error writing meta_ex file {meta_ex_file}")

