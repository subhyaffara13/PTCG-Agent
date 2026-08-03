import os

def generate_stub_for_py_module(
    mod: StubSource,
    target: str,
    *,
    parse_only: bool = False,
    inspect: bool = False,
    include_private: bool = False,
    export_less: bool = False,
    include_docstrings: bool = False,
    doc_dir: str = "",
    all_modules: list[str],
) -> None:
    """Use analysed (or just parsed) AST to generate type stub for single file.

    If directory for target doesn't exist it will created. Existing stub
    will be overwritten.
    """
    if inspect:
        ngen = InspectionStubGenerator(
            module_name=mod.module,
            known_modules=all_modules,
            _all_=mod.runtime_all,
            doc_dir=doc_dir,
            include_private=include_private,
            export_less=export_less,
            include_docstrings=include_docstrings,
        )
        ngen.generate_module()
        output = ngen.output()

    else:
        gen = ASTStubGenerator(
            mod.runtime_all,
            include_private=include_private,
            analyzed=not parse_only,
            export_less=export_less,
            include_docstrings=include_docstrings,
        )
        assert mod.ast is not None, "This function must be used only with analyzed modules"
        mod.ast.accept(gen)
        output = gen.output()

    # Write output to file.
    subdir = os.path.dirname(target)
    if subdir and not os.path.isdir(subdir):
        os.makedirs(subdir)
    with open(target, "w", encoding="utf-8") as file:
        file.write(output)

