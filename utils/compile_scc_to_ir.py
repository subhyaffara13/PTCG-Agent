
def compile_scc_to_ir(
    scc: list[MypyFile],
    result: BuildResult,
    mapper: Mapper,
    compiler_options: CompilerOptions,
    errors: Errors,
) -> ModuleIRs:
    """Compile an SCC into ModuleIRs.

    Any modules that this SCC depends on must have either been compiled,
    type checked, or loaded from a cache into mapper.

    Arguments:
        scc: The list of MypyFiles to compile
        result: The BuildResult from the mypy front-end
        mapper: The Mapper object mapping mypy ASTs to class and func IRs
        compiler_options: The compilation options
        errors: Where to report any errors encountered

    Returns the IR of the modules.
    """

    if compiler_options.verbose:
        print("Compiling {}".format(", ".join(x.name for x in scc)))

    # Generate basic IR, with missing exception and refcount handling.
    modules = build_ir(scc, result.graph, result.types, mapper, compiler_options, errors)
    if errors.num_errors > 0:
        return modules

    env_user_functions = {}
    for module in modules.values():
        for cls in module.classes:
            if cls.env_user_function:
                env_user_functions[cls.env_user_function] = cls

    for module in modules.values():
        module_path = result.graph[module.fullname].xpath
        for fn in module.functions:
            with catch_errors(module_path, fn.line):
                # Insert checks for uninitialized values.
                insert_uninit_checks(fn, compiler_options.strict_traceback_checks)
                # Insert exception handling.
                insert_exception_handling(fn, compiler_options.strict_traceback_checks)
                # Insert reference count handling.
                insert_ref_count_opcodes(fn)

                if fn in env_user_functions:
                    insert_spills(fn, env_user_functions[fn])

                if compiler_options.log_trace:
                    insert_event_trace_logging(fn, compiler_options)

                # Switch to lower abstraction level IR.
                lower_ir(fn, compiler_options)
                # Calculate implicit module dependencies (needed for librt)
                deps = find_implicit_op_dependencies(fn)
                if deps is not None:
                    module.dependencies.update(deps)
                # Perform optimizations.
                do_copy_propagation(fn, compiler_options)
                do_flag_elimination(fn, compiler_options)

        # Calculate implicit dependencies from class attribute types
        for cl in module.classes:
            deps = find_class_dependencies(cl)
            if deps is not None:
                module.dependencies.update(deps)

    return modules

