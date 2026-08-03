import os
import subprocess
import sys

def build_module(name: str, doc: str | None = None) -> nodes.Module:
    """create and initialize an astroid Module node"""
    node = nodes.Module(name, pure_python=False, package=False)
    node.postinit(
        body=[],
        doc_node=nodes.Const(value=doc) if doc else None,
    )
    return node


def build_module(source_files, options=[], skip=[], only=[], module_name=None):
    """
    Compile and import a f2py module, built from the given files.

    """

    code = f"import sys; sys.path = {sys.path!r}; import numpy.f2py; numpy.f2py.main()"

    d = get_module_dir()
    # gh-27045 : Skip if no compilers are found
    if not has_fortran_compiler():
        pytest.skip("No Fortran compiler available")

    # Copy files
    dst_sources = []
    f2py_sources = []
    for fn in source_files:
        if not os.path.isfile(fn):
            raise RuntimeError(f"{fn} is not a file")
        dst = os.path.join(d, os.path.basename(fn))
        shutil.copyfile(fn, dst)
        dst_sources.append(dst)

        base, ext = os.path.splitext(dst)
        if ext in (".f90", ".f95", ".f", ".c", ".pyf"):
            f2py_sources.append(dst)

    assert f2py_sources

    # Prepare options
    if module_name is None:
        module_name = get_temp_module_name()
    gil_options = []
    if '--freethreading-compatible' not in options and '--no-freethreading-compatible' not in options:
        # default to disabling the GIL if unset in options
        gil_options = ['--freethreading-compatible']
    f2py_opts = ["-c", "-m", module_name] + options + gil_options + f2py_sources
    f2py_opts += ["--backend", "meson"]
    if skip:
        f2py_opts += ["skip:"] + skip
    if only:
        f2py_opts += ["only:"] + only

    # Build
    cwd = os.getcwd()
    try:
        os.chdir(d)
        cmd = [sys.executable, "-c", code] + f2py_opts
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(f"Running f2py failed: {cmd[4:]}\n{asunicode(out)}")
    finally:
        os.chdir(cwd)

        # Partial cleanup
        for fn in dst_sources:
            os.unlink(fn)

    # Rebase (Cygwin-only)
    if sys.platform == "cygwin":
        # If someone starts deleting modules after import, this will
        # need to change to record how big each module is, rather than
        # relying on rebase being able to find that from the files.
        _module_list.extend(
            glob.glob(os.path.join(d, f"{module_name:s}*"))
        )
        subprocess.check_call(
            ["/usr/bin/rebase", "--database", "--oblivious", "--verbose"]
            + _module_list
        )

    # Import
    return import_module(module_name)

