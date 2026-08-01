
def _parse_local_package_name(path):
    # Determine the package name from a local directory
    pyproject_toml = os.path.join(path, "pyproject.toml")
    setup_py = os.path.join(path, "setup.py")
    has_pyproject = os.path.isfile(pyproject_toml)
    has_setup = os.path.isfile(setup_py)

    if not has_pyproject and not has_setup:
        raise PipError(
            f"{path} does not appear to be a Python project: "
            f"neither 'setup.py' nor 'pyproject.toml' found."
        )

    # Prefer the name in `pyproject.toml`
    if has_pyproject:
        with open(pyproject_toml, encoding="utf-8") as f:
            pp_toml = tomli.loads(f.read())
            name = pp_toml.get("project", {}).get("name")
            if name is not None:
                return name

    # Fall back on tokenizing setup.py and walk the syntax tree to find the
    # package name
    try:
        with open(os.path.join(path, "setup.py")) as f:
            tree = ast.parse(f.read())
        setup_kwargs = [
            expr.value.keywords
            for expr in tree.body
            if isinstance(expr, ast.Expr)
            and isinstance(expr.value, ast.Call)
            and expr.value.func.id == "setup"
        ][0]
        value = [kw.value for kw in setup_kwargs if kw.arg == "name"][0]
        return value.s
    except (IndexError, AttributeError, IOError, OSError):
        raise PipError(
            "Directory %r is not installable. "
            "Could not parse package name from 'setup.py'." % path
        )

