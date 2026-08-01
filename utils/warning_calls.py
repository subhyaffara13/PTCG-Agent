
def warning_calls():
    # combined "ignore" and stacklevel error
    base = Path(scipy.__file__).parent

    bad_filters = []
    bad_stacklevels = []

    for path in base.rglob("*.py"):
        # use tokenize to auto-detect encoding on systems where no
        # default encoding is defined (e.g., LANG='C')
        with tokenize.open(str(path)) as file:
            tree = ast.parse(file.read(), filename=str(path))
            finder = FindFuncs(path.relative_to(base))
            finder.visit(tree)
            bad_filters.extend(finder.bad_filters)
            bad_stacklevels.extend(finder.bad_stacklevels)

    return bad_filters, bad_stacklevels

