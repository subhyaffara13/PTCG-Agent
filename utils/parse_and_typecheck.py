
def parse_and_typecheck(
    sources: list[BuildSource],
    options: Options,
    compiler_options: CompilerOptions,
    groups: Groups,
    fscache: FileSystemCache | None = None,
    alt_lib_path: str | None = None,
) -> BuildResult:
    assert options.strict_optional, "strict_optional must be turned on"
    mypyc_plugin = MypycPlugin(options, compiler_options, groups)
    try:
        result = build(
            sources=sources,
            options=options,
            alt_lib_path=alt_lib_path,
            fscache=fscache,
            extra_plugins=[mypyc_plugin],
        )
    finally:
        mypyc_plugin.metastore.close()
    if result.errors:
        result.manager.metastore.close()
        raise CompileError(result.errors)
    return result

