
def mypycify(
    paths: list[str],
    *,
    only_compile_paths: Iterable[str] | None = None,
    verbose: bool = False,
    opt_level: str = "3",
    debug_level: str = "1",
    strip_asserts: bool = False,
    multi_file: bool = False,
    separate: bool | list[tuple[list[str], str | None]] = False,
    skip_cgen_input: (
        tuple[list[list[tuple[str, str]]], list[tuple[str, list[str], bool]]] | None
    ) = None,
    target_dir: str | None = None,
    include_runtime_files: bool | None = None,
    strict_dunder_typing: bool = False,
    group_name: str | None = None,
    log_trace: bool = False,
    depends_on_librt_internal: bool = False,
    install_librt: bool = False,
    experimental_features: bool = False,
) -> list[Extension]:
    """Main entry point to building using mypyc.

    This produces a list of Extension objects that should be passed as the
    ext_modules parameter to setup.

    Arguments:
        paths: A list of file paths to build. It may also contain mypy options.
        only_compile_paths: If not None, an iterable of paths that are to be
                            the only modules compiled, even if other modules
                            appear in the mypy command line given to paths.
                            (These modules must still be passed to paths.)

        verbose: Should mypyc be more verbose. Defaults to false.

        opt_level: The optimization level, as a string. Defaults to '3' (meaning '-O3').
        debug_level: The debug level, as a string. Defaults to '1' (meaning '-g1').
        strip_asserts: Should asserts be stripped from the generated code.

        multi_file: Should each Python module be compiled into its own C source file.
                    This can reduce compile time and memory requirements at the likely
                    cost of runtime performance of compiled code. Defaults to false.
        separate: Should compiled modules be placed in separate extension modules.
                  If False, all modules are placed in a single shared library.
                  If True, every module is placed in its own library.
                  Otherwise, separate should be a list of
                  (file name list, optional shared library name) pairs specifying
                  groups of files that should be placed in the same shared library
                  (while all other modules will be placed in its own library).

                  Each group can be compiled independently, which can
                  speed up compilation, but calls between groups can
                  be slower than calls within a group and can't be
                  inlined.
        target_dir: The directory to write C output files. Defaults to 'build'.
        include_runtime_files: If not None, whether the mypyc runtime library
                               should be directly #include'd instead of linked
                               separately in order to reduce compiler invocations.
                               Defaults to False in multi_file mode, True otherwise.
        strict_dunder_typing: If True, force dunder methods to have the return type
                              of the method strictly, which can lead to more
                              optimization opportunities. Defaults to False.
        group_name: If set, override the default group name derived from
                    the hash of module names. This is used for the names of the
                    output C files and the shared library. This is only supported
                    if there is a single group. [Experimental]
        log_trace: If True, compiled code writes a trace log of events in
                   mypyc_trace.txt (derived from executed operations). This is
                   useful for performance analysis, such as analyzing which
                   primitive ops are used the most and on which lines.
        depends_on_librt_internal: This is True only for mypy itself.
        install_librt: If True, also build the librt extension modules. Normally,
                       those are build and published on PyPI separately, but during
                       tests, we want to use their development versions (i.e. from
                       current commit).
        experimental_features: Enable experimental features (install_librt=True is
                               also needed if using experimental librt features). These
                               have no backward compatibility guarantees!
    """

    # Skip redundant inplace .so copies on every build_ext invocation.
    _patch_setuptools_copy_extensions_to_source()

    # Figure out our configuration
    compiler_options = CompilerOptions(
        strip_asserts=strip_asserts,
        multi_file=multi_file,
        verbose=verbose,
        separate=separate is not False,
        target_dir=target_dir,
        include_runtime_files=include_runtime_files,
        strict_dunder_typing=strict_dunder_typing,
        group_name=group_name,
        log_trace=log_trace,
        depends_on_librt_internal=depends_on_librt_internal,
        experimental_features=experimental_features,
    )

    # Generate all the actual important C code
    groups, group_cfilenames, source_deps = mypyc_build(
        paths,
        only_compile_paths=only_compile_paths,
        compiler_options=compiler_options,
        separate=separate,
        skip_cgen_input=skip_cgen_input,
    )

    # Mess around with setuptools and actually get the thing built
    setup_mypycify_vars()

    # Create a compiler object so we can make decisions based on what
    # compiler is being used. typeshed is missing some attributes on the
    # compiler object so we give it type Any
    compiler: Any = ccompiler.new_compiler()
    sysconfig.customize_compiler(compiler)

    build_dir = compiler_options.target_dir

    cflags = get_cflags(
        compiler_type=compiler.compiler_type,
        opt_level=opt_level,
        debug_level=debug_level,
        multi_file=multi_file,
        experimental_features=experimental_features,
        log_trace=log_trace,
    )

    # If configured to (defaults to yes in multi-file mode), copy the
    # runtime library in. Otherwise it just gets #included to save on
    # compiler invocations.
    shared_cfilenames = []
    include_dirs = set()
    if not compiler_options.include_runtime_files:
        # Collect all files to copy: runtime files + conditional source files
        files_to_copy = list(RUNTIME_C_FILES)
        for source_dep in source_deps:
            files_to_copy.append(source_dep.path)
            files_to_copy.append(source_dep.get_header())
            include_dirs.update(source_dep.include_dirs)

        if compiler_options.depends_on_librt_internal:
            files_to_copy.append("internal/librt_internal_api.h")
            files_to_copy.append("internal/librt_internal_api.c")
            include_dirs.add("internal")

        # Copy all files
        for name in files_to_copy:
            rt_file = os.path.join(build_dir, name)
            with open(os.path.join(include_dir(), name), encoding="utf-8") as f:
                write_file(rt_file, f.read())
            if name.endswith(".c"):
                shared_cfilenames.append(rt_file)

    extensions = []
    extra_include_dirs = [os.path.join(include_dir(), dir) for dir in include_dirs]
    for (group_sources, lib_name), (cfilenames, deps) in zip(groups, group_cfilenames):
        if lib_name:
            extensions.extend(
                build_using_shared_lib(
                    group_sources,
                    lib_name,
                    cfilenames + shared_cfilenames,
                    deps,
                    build_dir,
                    cflags,
                    extra_include_dirs,
                )
            )
        else:
            extensions.extend(
                build_single_module(
                    group_sources, cfilenames + shared_cfilenames, cflags, extra_include_dirs
                )
            )

    if install_librt:
        for name in RUNTIME_C_FILES:
            rt_file = os.path.join(build_dir, name)
            with open(os.path.join(include_dir(), name), encoding="utf-8") as f:
                write_file(rt_file, f.read())
        for mod, file_names, addit_files, includes in LIBRT_MODULES:
            for file_name in file_names + addit_files:
                rt_file = os.path.join(build_dir, file_name)
                with open(os.path.join(include_dir(), file_name), encoding="utf-8") as f:
                    write_file(rt_file, f.read())
            extensions.append(
                get_extension()(
                    mod,
                    sources=[
                        os.path.join(build_dir, file) for file in file_names + RUNTIME_C_FILES
                    ],
                    include_dirs=[include_dir()]
                    + [os.path.join(include_dir(), d) for d in includes],
                    extra_compile_args=cflags,
                )
            )

    # Tag every extension we own so the build_ext patch knows it's
    # safe to skip the redundant inplace copy for these specifically.
    for ext in extensions:
        setattr(ext, _MYPYC_EXTENSION_MARKER, True)

    return extensions

