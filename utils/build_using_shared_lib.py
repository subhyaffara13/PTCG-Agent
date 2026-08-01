
def build_using_shared_lib(
    sources: list[BuildSource],
    group_name: str,
    cfiles: list[str],
    deps: list[str],
    build_dir: str,
    extra_compile_args: list[str],
    extra_include_dirs: list[str],
) -> list[Extension]:
    """Produce the list of extension modules when a shared library is needed.

    This creates one shared library extension module that all the
    others import, and one shim extension module for each
    module in the build. Each shim simply calls an initialization function
    in the shared library.

    The shared library (which lib_name is the name of) is a Python
    extension module that exports the real initialization functions in
    Capsules stored in module attributes.
    """
    extensions = [
        get_extension()(
            shared_lib_name(group_name),
            sources=cfiles,
            include_dirs=[include_dir(), build_dir] + extra_include_dirs,
            depends=deps,
            extra_compile_args=extra_compile_args,
        )
    ]

    for source in sources:
        module_name = source.module.split(".")[-1]
        shim_file = generate_c_extension_shim(source.module, module_name, build_dir, group_name)

        # We include the __init__ in the "module name" we stick in the Extension,
        # since this seems to be needed for it to end up in the right place.
        full_module_name = source.module
        assert source.path
        if is_package_source(source):
            full_module_name += ".__init__"
        extensions.append(
            get_extension()(
                full_module_name, sources=[shim_file], extra_compile_args=extra_compile_args
            )
        )

    return extensions

