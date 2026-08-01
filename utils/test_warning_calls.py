
def test_warning_calls():
    # combined "ignore" and stacklevel error
    base = Path(numpy.__file__).parent

    for path in base.rglob("*.py"):
        if base / "testing" in path.parents:
            continue
        if path == base / "__init__.py":
            continue
        if path == base / "random" / "__init__.py":
            continue
        if path == base / "conftest.py":
            continue
        # use tokenize to auto-detect encoding on systems where no
        # default encoding is defined (e.g. LANG='C')
        with tokenize.open(str(path)) as file:
            tree = ast.parse(file.read())
            FindFuncs(path).visit(tree)

