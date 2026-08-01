
def _extern_libs_key(backend: Any) -> str:
    """Return a cache key fragment for extern libs (e.g. libdevice.10.bc).

    These files affect codegen but are not covered by triton_key() (Python
    sources only) or backend.hash() (ptxas version and arch only).
    """
    opts = backend.parse_options({})
    extern_libs = getattr(opts, "extern_libs", None)
    if not extern_libs:
        return ""
    parts = []
    for name, path in sorted(extern_libs):
        if os.path.isfile(path):
            with open(path, "rb") as f:
                parts.append(f"{name}-{hashlib.sha256(f.read()).hexdigest()}")
    return "-".join(parts)

