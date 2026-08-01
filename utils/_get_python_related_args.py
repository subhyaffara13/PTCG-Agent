
def _get_python_related_args() -> tuple[list[str], list[str]]:
    python_include_dirs = _get_python_include_dirs()
    python_include_path = sysconfig.get_path(
        "include", scheme="nt" if _IS_WINDOWS else "posix_prefix"
    )
    if python_include_path is not None:
        python_include_dirs.append(python_include_path)

    if _IS_WINDOWS:
        python_lib_path = [
            str(
                (
                    Path(sysconfig.get_path("include", scheme="nt")).parent / "libs"
                ).absolute()
            )
        ]
    else:
        python_lib_path = [sysconfig.get_config_var("LIBDIR")]

    if config.is_fbcode():
        python_include_dirs.append(build_paths.python_include)

    return python_include_dirs, python_lib_path

