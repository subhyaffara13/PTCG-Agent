import os

def write_cache(
    id: str,
    path: str,
    tree: MypyFile,
    dependencies: list[str],
    suppressed: list[str],
    suppressed_deps_opts: bytes,
    imports_ignored: dict[int, list[str]],
    dep_prios: list[int],
    dep_lines: list[int],
    old_interface_hash: bytes,
    trans_dep_hash: bytes,
    source_hash: str,
    ignore_all: bool,
    manager: BuildManager,
) -> tuple[bytes, tuple[CacheMeta, str] | None]:
    """Write cache files for a module.

    Note that this mypy's behavior is still correct when any given
    write_cache() call is replaced with a no-op, so error handling
    code that bails without writing anything is okay.

    Args:
      id: module ID
      path: module path
      tree: the fully checked module data
      dependencies: module IDs on which this module depends
      suppressed: module IDs which were suppressed as dependencies
      dep_prios: priorities (parallel array to dependencies)
      dep_lines: import line locations (parallel array to dependencies)
      old_interface_hash: the hash from the previous version of the data cache file
      source_hash: the hash of the source code
      ignore_all: the ignore_all flag for this module
      manager: the build manager (for pyversion, log/trace)

    Returns:
      A tuple containing the interface hash and inner tuple with CacheMeta
      that should be written and path to cache file (inner tuple may be None,
      if the cache data could not be written).
    """
    metastore = manager.metastore
    # For Bazel we use relative paths and zero mtimes.
    bazel = manager.options.bazel

    # Obtain file paths.
    meta_file, data_file, _ = get_cache_names(id, path, manager.options)
    manager.log(f"Writing {id} {path} {meta_file} {data_file}")

    # Update tree.path so that in bazel mode it's made relative (since
    # sometimes paths leak out).
    if bazel:
        tree.path = path

    plugin_data = manager.plugin.report_config_data(ReportConfigContext(id, path, is_check=False))

    # Serialize data and analyze interface
    if manager.options.fixed_format_cache:
        data_io = WriteBuffer()
        tree.write(data_io)
        data_bytes = data_io.getvalue()
    else:
        data = tree.serialize()
        data_bytes = json_dumps(data, manager.options.debug_cache)
    interface_hash = hash_digest_bytes(data_bytes + json_dumps(plugin_data))

    # Obtain and set up metadata
    st = manager.get_stat(path)
    if st is None:
        manager.log(f"Cannot get stat for {path}")
        # Remove apparently-invalid cache files.
        # (This is purely an optimization.)
        for filename in [data_file, meta_file]:
            try:
                os.remove(filename)
            except OSError:
                pass
        # Still return the interface hash we computed.
        return interface_hash, None

    # Write data cache file, if applicable
    # Note that for Bazel we don't record the data file's mtime.
    if old_interface_hash == interface_hash:
        manager.trace(f"Interface for {id} is unchanged")
    else:
        manager.trace(f"Interface for {id} has changed")
        if not metastore.write(data_file, data_bytes):
            # Most likely the error is the replace() call
            # (see https://github.com/python/mypy/issues/3215).
            manager.log(f"Error writing cache data file {data_file}")
            # Let's continue without writing the meta file.  Analysis:
            # If the replace failed, we've changed nothing except left
            # behind an extraneous temporary file; if the replace
            # worked but the getmtime() call failed, the meta file
            # will be considered invalid on the next run because the
            # data_mtime field won't match the data file's mtime.
            # Both have the effect of slowing down the next run a
            # little bit due to an out-of-date cache file.
            return interface_hash, None

    try:
        data_mtime = manager.getmtime(data_file)
    except OSError:
        manager.log(f"Error in os.stat({data_file!r}), skipping cache write")
        return interface_hash, None

    mtime = 0 if bazel else int(st.st_mtime)
    size = st.st_size
    # Note that the options we store in the cache are the options as
    # specified by the command line/config file and *don't* reflect
    # updates made by inline config directives in the file. This is
    # important, or otherwise the options would never match when
    # verifying the cache.
    assert source_hash is not None
    meta = CacheMeta(
        id=id,
        path=path,
        mtime=mtime,
        size=size,
        hash=source_hash,
        dependencies=dependencies,
        data_mtime=data_mtime,
        data_file=data_file,
        suppressed=suppressed,
        imports_ignored=imports_ignored,
        options=options_snapshot(id, manager),
        suppressed_deps_opts=suppressed_deps_opts,
        dep_prios=dep_prios,
        dep_lines=dep_lines,
        interface_hash=interface_hash,
        trans_dep_hash=trans_dep_hash,
        version_id=manager.version_id,
        ignore_all=ignore_all,
        plugin_data=plugin_data,
        # This one will be filled by the caller.
        dep_hashes=[],
    )
    return interface_hash, (meta, meta_file)


def write_cache(
    modules: ModuleIRs,
    result: BuildResult,
    group_map: dict[str, str | None],
    ctext: dict[str | None, list[tuple[str, str]]],
) -> None:
    """Write out the cache information for modules.

    Each module has the following cache information written (which is
    in addition to the cache information written by mypy itself):
      * A serialized version of its mypyc IR, minus the bodies of
        functions. This allows code that depends on it to use
        these serialized data structures when compiling against it
        instead of needing to recompile it. (Compiling against a
        module requires access to both its mypy and mypyc data
        structures.)
      * The hash of the mypy metadata cache file for the module.
        This is used to ensure that the mypyc cache and the mypy
        cache are in sync and refer to the same version of the code.
        This is particularly important if mypyc crashes/errors/is
        stopped after mypy has written its cache but before mypyc has.
      * The hashes of all the source file outputs for the group
        the module is in. This is so that the module will be
        recompiled if the source outputs are missing.
    """

    hashes = {}
    for name, files in ctext.items():
        hashes[name] = {file: compute_hash(data) for file, data in files}

    # Write out cache data
    for id, module in modules.items():
        st = result.graph[id]

        meta_path, _, _ = get_cache_names(id, st.xpath, result.manager.options)
        # If the metadata isn't there, skip writing the cache.
        try:
            meta_data = result.manager.metastore.read(meta_path)
        except OSError:
            continue

        newpath = get_state_ir_cache_name(st)
        ir_data = {
            "ir": module.serialize(),
            "meta_hash": hash_digest(meta_data),
            "src_hashes": hashes[group_map[id]],
        }

        result.manager.metastore.write(newpath, json_dumps(ir_data))

    result.manager.metastore.commit()

