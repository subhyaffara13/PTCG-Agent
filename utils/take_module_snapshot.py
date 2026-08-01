
def take_module_snapshot(module: types.ModuleType) -> str:
    """Take plugin module snapshot by recording its version and hash.

    We record _both_ hash and the version to detect more possible changes
    (e.g. if there is a change in modules imported by a plugin).
    """
    if hasattr(module, "__file__"):
        assert module.__file__ is not None
        with open(module.__file__, "rb") as f:
            digest = hash_digest(f.read())
    else:
        digest = "unknown"
    ver = getattr(module, "__version__", "none")
    return f"{ver}:{digest}"

