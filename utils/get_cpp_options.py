
def get_cpp_options(
    cpp_compiler: str,
    do_link: bool,
    warning_all: bool = True,
    extra_flags: Sequence[str] = (),
    min_optimize: bool = False,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    definitions: list[str] = []
    include_dirs: list[str] = []
    cflags: list[str] = []
    ldflags: list[str] = []
    libraries_dirs: list[str] = []
    libraries: list[str] = []
    passthrough_args: list[str] = []

    opt_cflags, opt_ldflags = _get_optimization_cflags(cpp_compiler, min_optimize)

    cflags = (
        opt_cflags
        + _get_shared_cflags(do_link)
        + _get_warning_all_cflag(warning_all)
        + _get_cpp_std_cflag()
        + _get_os_related_cpp_cflags(cpp_compiler)
    )

    definitions += _get_os_related_cpp_definitions(cpp_compiler)

    if not _IS_WINDOWS and config.aot_inductor.enable_lto and _is_clang(cpp_compiler):
        ldflags.append("fuse-ld=lld")
        ldflags.append("flto=thin")

    passthrough_args.append(" ".join(extra_flags))

    if config.aot_inductor.cross_target_platform == "windows":
        passthrough_args.extend(["-static-libstdc++", "-static-libgcc"])
        if check_mingw_win32_flavor(MINGW_GXX) == "posix":
            passthrough_args.append("-Wl,-Bstatic -lwinpthread -Wl,-Bdynamic")

    return (
        definitions,
        include_dirs,
        cflags,
        ldflags + opt_ldflags,
        libraries_dirs,
        libraries,
        passthrough_args,
    )

