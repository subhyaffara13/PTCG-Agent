
def execfile(filename, glob):
    # We use execfile() (here rewritten for Python 3) instead of
    # __import__() to load the build script.  The problem with
    # a normal import is that in some packages, the intermediate
    # __init__.py files may already try to import the file that
    # we are generating.
    with open(filename) as f:
        src = f.read()
    src += '\n'      # Python 2.6 compatibility
    code = compile(src, filename, 'exec')
    exec(code, glob, glob)


def execfile(fname: str, glob: dict[str, Any]) -> None:
    with open(fname, "rb") as f:
        exec(compile(f.read(), fname, "exec"), glob, glob)  # noqa: S102

