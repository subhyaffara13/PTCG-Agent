
def compile_modules_to_c(
    result: BuildResult, compiler_options: CompilerOptions, errors: Errors, groups: Groups
) -> tuple[ModuleIRs, list[FileContents], Mapper]:
    """Compile Python module(s) to the source of Python C extension modules.

    This generates the source code for the "shared library" module
    for each group. The shim modules are generated in mypyc.build.
    Each shared library module provides, for each module in its group,
    a PyCapsule containing an initialization function.
    Additionally, it provides a capsule containing an export table of
    pointers to all the group's functions and static variables.

    Arguments:
        result: The BuildResult from the mypy front-end
        compiler_options: The compilation options
        errors: Where to report any errors encountered
        groups: The groups that we are compiling. See documentation of Groups type above.

    Returns the IR of the modules and a list containing the generated files for each group.
    """
    # Construct a map from modules to what group they belong to
    group_map = {source.module: lib_name for group, lib_name in groups for source in group}
    mapper = Mapper(group_map)

    # Sometimes when we call back into mypy, there might be errors.
    # We don't want to crash when that happens.
    result.manager.errors.set_file(
        "<mypyc>", module=None, scope=None, options=result.manager.options
    )

    modules = compile_modules_to_ir(result, mapper, compiler_options, errors)
    if errors.num_errors > 0:
        return {}, [], Mapper({})

    ctext = compile_ir_to_c(groups, modules, result, mapper, compiler_options)
    write_cache(modules, result, group_map, ctext)

    return modules, [ctext[name] for _, name in groups], mapper

