
def compile_ir_to_c(
    groups: Groups,
    modules: ModuleIRs,
    result: BuildResult,
    mapper: Mapper,
    compiler_options: CompilerOptions,
) -> dict[str | None, list[tuple[str, str]]]:
    """Compile a collection of ModuleIRs to C source text.

    Returns a dictionary mapping group names to a list of (file name,
    file text) pairs.
    """
    source_paths = {
        source.module: result.graph[source.module].xpath
        for sources, _ in groups
        for source in sources
    }

    names = NameGenerator(
        [[source.module for source in sources] for sources, _ in groups],
        separate=compiler_options.separate,
    )

    # Generate C code for each compilation group. Each group will be
    # compiled into a separate extension module.
    ctext: dict[str | None, list[tuple[str, str]]] = {}
    for group_sources, group_name in groups:
        group_modules = {
            source.module: modules[source.module]
            for source in group_sources
            if source.module in modules
        }
        if not group_modules:
            # Fully-cached group (e.g. pip's second setup.py invoke for
            # the wheel phase): no fresh IR was produced. Reuse the file
            # list recorded in any module's IR cache so the linker still
            # sees the previous run's outputs; empty content is a "do
            # not rewrite" sentinel for mypyc_build.
            ctext[group_name] = _load_cached_group_files(group_sources, result)
            continue
        generator = GroupGenerator(
            group_modules, source_paths, group_name, mapper.group_map, names, compiler_options
        )
        ctext[group_name] = generator.generate_c_for_modules()

    return ctext

