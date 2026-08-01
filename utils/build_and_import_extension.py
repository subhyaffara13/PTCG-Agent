
def build_and_import_extension(
        modname, functions, *, prologue="", build_dir=None,
        include_dirs=None, more_init=""):
    """
    Build and imports a c-extension module `modname` from a list of function
    fragments `functions`.


    Parameters
    ----------
    functions : list of fragments
        Each fragment is a sequence of func_name, calling convention, snippet.
    prologue : string
        Code to precede the rest, usually extra ``#include`` or ``#define``
        macros.
    build_dir : pathlib.Path
        Where to build the module, usually a temporary directory
    include_dirs : list
        Extra directories to find include files when compiling
    more_init : string
        Code to appear in the module PyMODINIT_FUNC

    Returns
    -------
    out: module
        The module will have been loaded and is ready for use

    Examples
    --------
    >>> functions = [("test_bytes", "METH_O", \"\"\"
        if ( !PyBytesCheck(args)) {
            Py_RETURN_FALSE;
        }
        Py_RETURN_TRUE;
    \"\"\")]
    >>> mod = build_and_import_extension("testme", functions)
    >>> assert not mod.test_bytes('abc')
    >>> assert mod.test_bytes(b'abc')
    """
    if include_dirs is None:
        include_dirs = []
    body = prologue + _make_methods(functions, modname)
    init = """
    PyObject *mod = PyModule_Create(&moduledef);
    #ifdef Py_GIL_DISABLED
    PyUnstable_Module_SetGIL(mod, Py_MOD_GIL_NOT_USED);
    #endif
           """
    if not build_dir:
        build_dir = pathlib.Path('.')
    if more_init:
        init += """#define INITERROR return NULL
                """
        init += more_init
    init += "\nreturn mod;"
    source_string = _make_source(modname, init, body)
    mod_so = compile_extension_module(
        modname, build_dir, include_dirs, source_string)
    import importlib.util
    spec = importlib.util.spec_from_file_location(modname, mod_so)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

