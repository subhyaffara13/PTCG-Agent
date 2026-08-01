
def get_cflags(
    *,
    compiler_type: str | None = None,
    opt_level: str = "3",
    debug_level: str = "1",
    multi_file: bool = False,
    experimental_features: bool = False,
    log_trace: bool = False,
) -> list[str]:
    """Get C compiler flags for the given configuration.

    Args:
        compiler_type: Compiler type, e.g. "unix" or "msvc". If None, detected automatically.
        opt_level: Optimization level as string ("0", "1", "2", or "3").
        debug_level: Debug level as string ("0", "1", "2", or "3").
        multi_file: Whether multi-file compilation mode is enabled.
        experimental_features: Whether experimental features are enabled.
        log_trace: Whether trace logging is enabled.

    Returns:
        List of compiler flags.
    """
    if compiler_type is None:
        compiler: Any = ccompiler.new_compiler()
        sysconfig.customize_compiler(compiler)
        compiler_type = compiler.compiler_type

    cflags: list[str] = []
    if compiler_type == "unix":
        cflags += [
            f"-O{opt_level}",
            f"-g{debug_level}",
            "-Werror",
            "-Wno-unused-function",
            "-Wno-unused-label",
            "-Wno-unreachable-code",
            "-Wno-unused-variable",
            "-Wno-unused-command-line-argument",
            "-Wno-unknown-warning-option",
            "-Wno-unused-but-set-variable",
            "-Wno-ignored-optimization-argument",
            # GCC at -O3 false-positives on struct hack (items[1]) in vec buffers
            "-Wno-array-bounds",
            "-Wno-stringop-overread",
            "-Wno-stringop-overflow",
            # Disables C Preprocessor (cpp) warnings
            # See https://github.com/mypyc/mypyc/issues/956
            "-Wno-cpp",
            "-Wno-array-bounds",
            "-Wno-stringop-overread",
            "-Wno-stringop-overflow",
        ]
        if log_trace:
            cflags.append("-DMYPYC_LOG_TRACE")
        if experimental_features:
            cflags.append("-DMYPYC_EXPERIMENTAL")
        if opt_level == "0":
            cflags.append("-UNDEBUG")
    elif compiler_type == "msvc":
        # msvc doesn't have levels, '/O2' is full and '/Od' is disable
        if opt_level == "0":
            opt_level = "d"
            cflags.append("/UNDEBUG")
        elif opt_level in ("1", "2", "3"):
            opt_level = "2"
        if debug_level == "0":
            debug_level = "NONE"
        elif debug_level == "1":
            debug_level = "FASTLINK"
        elif debug_level in ("2", "3"):
            debug_level = "FULL"
        cflags += [
            f"/O{opt_level}",
            f"/DEBUG:{debug_level}",
            "/wd4102",  # unreferenced label
            "/wd4101",  # unreferenced local variable
            "/wd4146",  # negating unsigned int
        ]
        if multi_file:
            # Disable whole program optimization in multi-file mode so
            # that we actually get the compilation speed and memory
            # use wins that multi-file mode is intended for.
            cflags += ["/GL-", "/wd9025"]  # warning about overriding /GL
        if log_trace:
            cflags.append("/DMYPYC_LOG_TRACE")
        if experimental_features:
            cflags.append("/DMYPYC_EXPERIMENTAL")
    return cflags

