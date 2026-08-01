
def build_single_module(
    sources: list[BuildSource],
    cfiles: list[str],
    extra_compile_args: list[str],
    extra_include_dirs: list[str],
) -> list[Extension]:
    """Produce the list of extension modules for a standalone extension.

    This contains just one module, since there is no need for a shared module.
    """
    return [
        get_extension()(
            sources[0].module,
            sources=cfiles,
            include_dirs=[include_dir()] + extra_include_dirs,
            extra_compile_args=extra_compile_args,
        )
    ]

