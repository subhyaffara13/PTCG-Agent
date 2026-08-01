
def parse_source_file(mod: StubSource, mypy_options: MypyOptions) -> None:
    """Parse a source file.

    On success, store AST in the corresponding attribute of the stub source.
    If there are syntax errors, print them and exit.
    """
    assert mod.path is not None, "Not found module was not skipped"
    with open(mod.path, "rb") as f:
        data = f.read()
    source = mypy.util.decode_python_encoding(data)
    errors = Errors(mypy_options)
    mod.ast = mypy.parse.parse(
        source, fnam=mod.path, module=mod.module, errors=errors, options=mypy_options, eager=True
    )
    mod.ast._fullname = mod.module
    if errors.is_blockers():
        # Syntax error!
        for m in errors.new_messages():
            sys.stderr.write(f"{m}\n")
        sys.exit(1)

