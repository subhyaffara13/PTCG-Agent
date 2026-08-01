
def _librt_build_hash(experimental: bool, opt_level: str) -> str:
    """Compute hash for librt build, including sources and build environment."""
    # Import lazily to ensure mypyc.build has ensured that distutils is correctly set up
    from distutils import ccompiler

    h = hashlib.sha256()
    # Include experimental flag
    h.update(b"exp" if experimental else b"noexp")
    h.update(f"opt={opt_level}".encode())
    # Include full Python version string (includes git hash for dev builds)
    h.update(sys.version.encode())
    # Include debug build status (gettotalrefcount only exists in debug builds)
    is_debug = hasattr(sys, "gettotalrefcount")
    h.update(b"debug" if is_debug else b"release")
    # Include free-threading status (Python 3.13+)
    is_free_threaded = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
    h.update(b"freethreaded" if is_free_threaded else b"gil")
    # Include compiler type (e.g., "unix" or "msvc")
    compiler: Any = ccompiler.new_compiler()
    h.update(compiler.compiler_type.encode())
    # Include environment variables that affect C compilation
    for var in ("CC", "CXX", "CFLAGS", "CPPFLAGS", "LDFLAGS"):
        val = os.environ.get(var, "")
        h.update(f"{var}={val}".encode())
    # Hash runtime files
    for name in RUNTIME_C_FILES:
        path = os.path.join(include_dir(), name)
        h.update(name.encode() + b"|")
        with open(path, "rb") as f:
            h.update(f.read())
    # Hash librt module files
    for mod, files, extra, includes in LIBRT_MODULES:
        for fname in files + extra:
            path = os.path.join(include_dir(), fname)
            h.update(fname.encode() + b"|")
            with open(path, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:16]

