
def convert_binary_cache_meta_to_json(data: bytes, data_file: str) -> Json:
    assert (
        data[0] == cache_version() and data[1] == CACHE_VERSION
    ), "Cache file created by an incompatible mypy version"
    meta = CacheMeta.read(ReadBuffer(data[2:]), data_file)
    assert meta is not None, f"Error reading meta cache file associated with {data_file}"
    return {
        "id": meta.id,
        "path": meta.path,
        "mtime": meta.mtime,
        "size": meta.size,
        "hash": meta.hash,
        "data_mtime": meta.data_mtime,
        "dependencies": meta.dependencies,
        "suppressed": meta.suppressed,
        "options": meta.options,
        "dep_prios": meta.dep_prios,
        "dep_lines": meta.dep_lines,
        "dep_hashes": [dep.hex() for dep in meta.dep_hashes],
        "interface_hash": meta.interface_hash.hex(),
        "version_id": meta.version_id,
        "ignore_all": meta.ignore_all,
        "plugin_data": meta.plugin_data,
    }

