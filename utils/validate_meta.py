import time

def validate_meta(
    meta: CacheMeta | None, id: str, path: str | None, ignore_all: bool, manager: BuildManager
) -> CacheMeta | None:
    """Checks whether the cached AST of this module can be used.

    Returns:
      None, if the cached AST is unusable.
      Original meta, if mtime/size matched.
      Meta with mtime updated to match source file, if hash/size matched but mtime/path didn't.
    """
    # This requires two steps. The first one is obvious: we check that the module source file
    # contents is the same as it was when the cache data file was created. The second one is not
    # too obvious: we check that the cache data file mtime has not changed; it is needed because
    # we use cache data file mtime to propagate information about changes in the dependencies.

    if meta is None:
        manager.log(f"Metadata not found for {id}")
        return None

    if meta.ignore_all and not ignore_all:
        manager.log(f"Metadata abandoned for {id}: errors were previously ignored")
        return None

    if manager.stats_enabled:
        t0 = time.time()
    bazel = manager.options.bazel
    assert path is not None, "Internal error: meta was provided without a path"
    if not manager.options.skip_cache_mtime_checks:
        # Check data_file; assume if its mtime matches it's good.
        try:
            data_mtime = manager.getmtime(meta.data_file)
        except OSError:
            manager.log(f"Metadata abandoned for {id}: failed to stat data_file")
            return None
        if data_mtime != meta.data_mtime:
            manager.log(f"Metadata abandoned for {id}: data cache is modified")
            return None

    if bazel:
        # Normalize path under bazel to make sure it isn't absolute
        path = normpath(path, manager.options)

    st = manager.get_stat(path)
    if st is None:
        return None
    if not stat.S_ISDIR(st.st_mode) and not stat.S_ISREG(st.st_mode):
        manager.log(f"Metadata abandoned for {id}: file or directory {path} does not exist")
        return None

    if manager.stats_enabled:
        manager.add_stats(validate_stat_time=time.time() - t0)

    # When we are using a fine-grained cache, we want our initial
    # build() to load all of the cache information and then do a
    # fine-grained incremental update to catch anything that has
    # changed since the cache was generated. We *don't* want to do a
    # coarse-grained incremental rebuild, so we accept the cache
    # metadata even if it doesn't match the source file.
    #
    # We still *do* the mtime/hash checks, however, to enable
    # fine-grained mode to take advantage of the mtime-updating
    # optimization when mtimes differ but hashes match.  There is
    # essentially no extra time cost to computing the hash here, since
    # it will be cached and will be needed for finding changed files
    # later anyways.
    fine_grained_cache = manager.use_fine_grained_cache()

    size = st.st_size
    # Bazel ensures the cache is valid.
    if size != meta.size and not bazel and not fine_grained_cache:
        manager.log(f"Metadata abandoned for {id}: file {path} has different size")
        return None

    # Bazel ensures the cache is valid.
    mtime = 0 if bazel else int(st.st_mtime)
    if not bazel and (mtime != meta.mtime or path != meta.path):
        if manager.quickstart_state and path in manager.quickstart_state:
            # If the mtime and the size of the file recorded in the quickstart dump matches
            # what we see on disk, we know (assume) that the hash matches the quickstart
            # data as well. If that hash matches the hash in the metadata, then we know
            # the file is up to date even though the mtime is wrong, without needing to hash it.
            qmtime, qsize, qhash = manager.quickstart_state[path]
            if int(qmtime) == mtime and qsize == size and qhash == meta.hash:
                manager.log(f"Metadata fresh (by quickstart) for {id}: file {path}")
                meta.mtime = mtime
                meta.path = path
                return meta

        t0 = time.time()
        try:
            # dir means it is a namespace package
            if stat.S_ISDIR(st.st_mode):
                source_hash = ""
            else:
                source_hash = manager.fscache.hash_digest(path)
        except (OSError, UnicodeDecodeError, DecodeError):
            return None
        manager.add_stats(validate_hash_time=time.time() - t0)
        if source_hash != meta.hash:
            if fine_grained_cache:
                manager.log(f"Using stale metadata for {id}: file {path}")
                return meta
            else:
                manager.log(f"Metadata abandoned for {id}: file {path} has different hash")
                return None
        else:
            if manager.stats_enabled:
                t0 = time.time()
            # Optimization: update mtime and path (otherwise, this mismatch will reappear).
            meta.mtime = mtime
            meta.path = path
            meta.size = size
            meta.options = options_snapshot(id, manager)
            meta_file, _, _ = get_cache_names(id, path, manager.options)
            if manager.logging_enabled:
                manager.log(
                    "Updating mtime for {}: file {}, meta {}, mtime {}".format(
                        id, path, meta_file, meta.mtime
                    )
                )
            write_cache_meta(meta, manager, meta_file)
            if manager.stats_enabled:
                t1 = time.time()
                manager.add_stats(
                    validate_update_time=time.time() - t1, validate_munging_time=t1 - t0
                )
            return meta

    # It's a match on (id, path, size, hash, mtime).
    if manager.logging_enabled:
        manager.log(f"Metadata fresh for {id}: file {path}")
    return meta

