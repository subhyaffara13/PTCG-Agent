
def default_lib_path(
    data_dir: str, pyversion: tuple[int, int], custom_typeshed_dir: str | None
) -> list[str]:
    """Return default standard library search paths. Guaranteed to be normalised."""

    data_dir = os.path.abspath(data_dir)
    path: list[str] = []

    if custom_typeshed_dir:
        custom_typeshed_dir = os.path.abspath(custom_typeshed_dir)
        typeshed_dir = os.path.join(custom_typeshed_dir, "stdlib")
        mypy_extensions_dir = os.path.join(custom_typeshed_dir, "stubs", "mypy-extensions")
        librt_dir = os.path.join(custom_typeshed_dir, "stubs", "librt")
        versions_file = os.path.join(typeshed_dir, "VERSIONS")
        if not os.path.isdir(typeshed_dir) or not os.path.isfile(versions_file):
            print(
                "error: --custom-typeshed-dir does not point to a valid typeshed ({})".format(
                    custom_typeshed_dir
                ),
                file=sys.stderr,
            )
            sys.exit(2)
    else:
        auto = os.path.join(data_dir, "stubs-auto")
        if os.path.isdir(auto):
            data_dir = auto
        typeshed_dir = os.path.join(data_dir, "typeshed", "stdlib")
        mypy_extensions_dir = os.path.join(data_dir, "typeshed", "stubs", "mypy-extensions")
        librt_dir = os.path.join(data_dir, "typeshed", "stubs", "librt")
    path.append(typeshed_dir)

    # Get mypy-extensions and librt stubs from typeshed, since we treat them as
    # "internal" libraries, similar to typing and typing-extensions.
    path.append(mypy_extensions_dir)
    path.append(librt_dir)

    # Add fallback path that can be used if we have a broken installation.
    if sys.platform != "win32":
        path.append("/usr/local/lib/mypy")
    if not path:
        print(
            "Could not resolve typeshed subdirectories. Your mypy install is broken.\n"
            "Python executable is located at {}.\nMypy located at {}".format(
                sys.executable, data_dir
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    return path

