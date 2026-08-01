
def resolve_collection_argument(
    invocation_path: Path,
    arg: str,
    arg_index: int,
    *,
    as_pypath: bool = False,
    consider_namespace_packages: bool = False,
) -> CollectionArgument:
    """Parse path arguments optionally containing selection parts and return (fspath, names).

    Command-line arguments can point to files and/or directories, and optionally contain
    parts for specific tests selection, for example:

        "pkg/tests/test_foo.py::TestClass::test_foo"

    This function ensures the path exists, and returns a resolved `CollectionArgument`:

        CollectionArgument(
            path=Path("/full/path/to/pkg/tests/test_foo.py"),
            parts=["TestClass", "test_foo"],
            module_name=None,
        )

    When as_pypath is True, expects that the command-line argument actually contains
    module paths instead of file-system paths:

        "pkg.tests.test_foo::TestClass::test_foo[a,b]"

    In which case we search sys.path for a matching module, and then return the *path* to the
    found module, which may look like this:

        CollectionArgument(
            path=Path("/home/u/myvenv/lib/site-packages/pkg/tests/test_foo.py"),
            parts=["TestClass", "test_foo"],
            parametrization="[a,b]",
            module_name="pkg.tests.test_foo",
        )

    If the path doesn't exist, raise UsageError.
    If the path is a directory and selection parts are present, raise UsageError.
    """
    base, squacket, rest = arg.partition("[")
    strpath, *parts = base.split("::")
    if squacket and not parts:
        raise UsageError(f"path cannot contain [] parametrization: {arg}")
    parametrization = f"{squacket}{rest}" if squacket else None
    module_name = None
    if as_pypath:
        pyarg_strpath = search_pypath(
            strpath, consider_namespace_packages=consider_namespace_packages
        )
        if pyarg_strpath is not None:
            module_name = strpath
            strpath = pyarg_strpath
    fspath = invocation_path / strpath
    fspath = absolutepath(fspath)
    if not safe_exists(fspath):
        msg = (
            "module or package not found: {arg} (missing __init__.py?)"
            if as_pypath
            else "file or directory not found: {arg}"
        )
        raise UsageError(msg.format(arg=arg))
    if parts and fspath.is_dir():
        msg = (
            "package argument cannot contain :: selection parts: {arg}"
            if as_pypath
            else "directory argument cannot contain :: selection parts: {arg}"
        )
        raise UsageError(msg.format(arg=arg))
    return CollectionArgument(
        path=fspath,
        parts=parts,
        parametrization=parametrization,
        module_name=module_name,
        original_index=arg_index,
    )

