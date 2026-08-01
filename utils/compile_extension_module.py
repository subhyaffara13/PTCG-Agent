
def compile_extension_module(
        name, builddir, include_dirs,
        source_string, libraries=None, library_dirs=None):
    """
    Build an extension module and return the filename of the resulting
    native code file.

    Parameters
    ----------
    name : string
        name of the module, possibly including dots if it is a module inside a
        package.
    builddir : pathlib.Path
        Where to build the module, usually a temporary directory
    include_dirs : list
        Extra directories to find include files when compiling
    libraries : list
        Libraries to link into the extension module
    library_dirs: list
        Where to find the libraries, ``-L`` passed to the linker
    """
    modname = name.split('.')[-1]
    dirname = builddir / name
    dirname.mkdir(exist_ok=True)
    cfile = _convert_str_to_file(source_string, dirname)
    include_dirs = include_dirs or []
    libraries = libraries or []
    library_dirs = library_dirs or []

    return _c_compile(
        cfile, outputfilename=dirname / modname,
        include_dirs=include_dirs, libraries=libraries,
        library_dirs=library_dirs,
        )

