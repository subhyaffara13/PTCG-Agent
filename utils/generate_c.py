import sys
import time

def generate_c(
    sources: list[BuildSource],
    options: Options,
    groups: emitmodule.Groups,
    fscache: FileSystemCache,
    compiler_options: CompilerOptions,
) -> tuple[list[list[tuple[str, str]]], str, list[SourceDep]]:
    """Drive the actual core compilation step.

    The groups argument describes how modules are assigned to C
    extension modules. See the comments on the Groups type in
    mypyc.emitmodule for details.

    Returns the C source code, (for debugging) the pretty printed IR, and list of SourceDeps.
    """
    t0 = time.time()

    try:
        result = emitmodule.parse_and_typecheck(
            sources, options, compiler_options, groups, fscache
        )
    except CompileError as e:
        emit_messages(options, e.messages, time.time() - t0, serious=(not e.use_stdout))
        sys.exit(1)

    try:
        t1 = time.time()
        if result.errors:
            emit_messages(options, result.errors, t1 - t0)
            sys.exit(1)

        if compiler_options.verbose:
            print(f"Parsed and typechecked in {t1 - t0:.3f}s")

        errors = Errors(options)
        modules, ctext, mapper = emitmodule.compile_modules_to_c(
            result, compiler_options=compiler_options, errors=errors, groups=groups
        )
        t2 = time.time()
        emit_messages(options, errors.new_messages(), t2 - t1)
        if errors.num_errors:
            # No need to stop the build if only warnings were emitted.
            sys.exit(1)

        if compiler_options.verbose:
            print(f"Compiled to C in {t2 - t1:.3f}s")

        if options.mypyc_annotation_file:
            generate_annotated_html(options.mypyc_annotation_file, result, modules, mapper)

        # Collect SourceDep dependencies
        source_deps = sorted(emitmodule.collect_source_dependencies(modules), key=lambda d: d.path)
        return ctext, "\n".join(format_modules(modules)), source_deps
    finally:
        result.manager.metastore.close()

