import os

def compile_link_import_py_ext(sources, extname=None, build_dir='.', compile_kwargs=None,
                               link_kwargs=None, extra_objs=None):
    """ Compiles sources to a shared object (Python extension) and imports it

    Sources in ``sources`` which is imported. If shared object is newer than the sources, they
    are not recompiled but instead it is imported.

    Parameters
    ==========

    sources : list of strings
        List of paths to sources.
    extname : string
        Name of extension (default: ``None``).
        If ``None``: taken from the last file in ``sources`` without extension.
    build_dir: str
        Path to directory in which objects files etc. are generated.
    compile_kwargs: dict
        keyword arguments passed to ``compile_sources``
    link_kwargs: dict
        keyword arguments passed to ``link_py_so``
    extra_objs: list
        List of paths to (prebuilt) object files / static libraries to link against.

    Returns
    =======

    The imported module from of the Python extension.
    """
    if extname is None:
        extname = os.path.splitext(os.path.basename(sources[-1]))[0]

    compile_kwargs = compile_kwargs or {}
    link_kwargs = link_kwargs or {}

    try:
        mod = import_module_from_file(os.path.join(build_dir, extname), sources)
    except ImportError:
        objs = compile_sources(list(map(get_abspath, sources)), destdir=build_dir,
                               cwd=build_dir, **compile_kwargs)
        so = link_py_so(objs, cwd=build_dir, fort=any_fortran_src(sources),
                        cplus=any_cplus_src(sources), extra_objs=extra_objs, **link_kwargs)
        mod = import_module_from_file(so)
    return mod

