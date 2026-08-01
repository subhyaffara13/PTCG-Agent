
def build_ir_for_single_file2(
    input_lines: list[str], compiler_options: CompilerOptions | None = None
) -> tuple[ModuleIR, MypyFile, dict[Expression, Type], Mapper]:
    program_text = "\n".join(input_lines)

    # By default generate IR compatible with the earliest supported Python C API.
    # If a test needs more recent API features, this should be overridden.
    compiler_options = compiler_options or CompilerOptions(capi_version=(3, 10))
    options = Options()
    options.show_traceback = True
    options.hide_error_codes = True
    options.use_builtins_fixtures = True
    options.strict_optional = True
    options.python_version = compiler_options.python_version or (3, 10)
    options.export_types = True
    options.preserve_asts = True
    options.allow_empty_bodies = True
    options.strict_bytes = True
    options.disable_bytearray_promotion = True
    options.disable_memoryview_promotion = True
    options.per_module_options["__main__"] = {"mypyc": True}

    source = build.BuildSource("main", "__main__", program_text)
    # Construct input as a single single.
    # Parse and type check the input program.
    result = build.build(sources=[source], options=options, alt_lib_path=test_temp_dir)
    result.manager.metastore.close()
    if result.errors:
        raise CompileError(result.errors)

    errors = Errors(options)
    mapper = Mapper({"__main__": None})
    modules = build_ir(
        [result.files["__main__"]], result.graph, result.types, mapper, compiler_options, errors
    )
    if errors.num_errors:
        raise CompileError(errors.new_messages())

    module = list(modules.values())[0]
    for fn in module.functions:
        assert_func_ir_valid(fn)
    tree = result.graph[module.fullname].tree
    assert tree is not None
    return module, tree, result.types, mapper

