
def generate_stub_for_c_module(
    module_name: str,
    target: str,
    known_modules: list[str],
    doc_dir: str = "",
    *,
    include_private: bool = False,
    export_less: bool = False,
    include_docstrings: bool = False,
) -> None:
    """Generate stub for C module.

    Signature generators are called in order until a list of signatures is returned.  The order
    is:
    - signatures inferred from .rst documentation (if given)
    - simple runtime introspection (looking for docstrings and attributes
      with simple builtin types)
    - fallback based special method names or "(*args, **kwargs)"

    If directory for target doesn't exist it will be created. Existing stub
    will be overwritten.
    """
    subdir = os.path.dirname(target)
    if subdir and not os.path.isdir(subdir):
        os.makedirs(subdir)

    gen = InspectionStubGenerator(
        module_name,
        known_modules,
        doc_dir,
        include_private=include_private,
        export_less=export_less,
        include_docstrings=include_docstrings,
    )
    gen.generate_module()
    output = gen.output()

    with open(target, "w", encoding="utf-8") as file:
        file.write(output)

