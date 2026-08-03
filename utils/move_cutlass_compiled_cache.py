import os

def move_cutlass_compiled_cache() -> None:
    """Move CUTLASS compiled cache file to the cache directory if it exists."""
    if try_import_cutlass.cache_info().currsize == 0:
        return

    try:
        import cutlass_cppgen  # type: ignore[import-not-found]
    except ImportError:
        return

    # Check if the CACHE_FILE attribute exists in cutlass_cppgen and if the file exists
    if not hasattr(cutlass_cppgen, "CACHE_FILE") or not os.path.exists(
        cutlass_cppgen.CACHE_FILE
    ):
        return

    try:
        filename = os.path.basename(cutlass_cppgen.CACHE_FILE)
        shutil.move(cutlass_cppgen.CACHE_FILE, os.path.join(cache_dir(), filename))
        log.debug("Moved CUTLASS compiled cache file to %s", cache_dir())
    except OSError:
        log.warning("Failed to move CUTLASS compiled cache file", exc_info=True)

