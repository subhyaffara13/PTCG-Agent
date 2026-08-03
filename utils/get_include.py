import os

def get_include(user: bool = False) -> str:  # noqa: ARG001
    """
    Return the path to the pybind11 include directory. The historical "user"
    argument is unused, and may be removed.
    """
    installed_path = os.path.join(DIR, "include")
    source_path = os.path.join(os.path.dirname(DIR), "include")
    return installed_path if os.path.exists(installed_path) else source_path


def get_include(user: bool = False) -> str:  # noqa: ARG001
    """
    Return the path to the pybind11 include directory. The historical "user"
    argument is unused, and may be removed.
    """
    installed_path = os.path.join(DIR, "include")
    source_path = os.path.join(os.path.dirname(DIR), "include")
    return installed_path if os.path.exists(installed_path) else source_path


def get_include():
    """
    Return the directory that contains the ``fortranobject.c`` and ``.h`` files.

    Python extension modules built with f2py-generated code need to use
    ``fortranobject.c`` as a source file, and include the ``fortranobject.h``
    header. This function can be used to obtain the directory containing
    both of these files.

    Returns
    -------
    include_path : str
        Absolute path to the directory containing ``fortranobject.c`` and
        ``fortranobject.h``.

    Notes
    -----
    .. versionadded:: 1.21.1

    Unless the build system you are using has specific support for f2py,
    building a Python extension using a ``.pyf`` signature file is a two-step
    process. For a module ``mymod``:

    * Step 1: run ``python -m numpy.f2py mymod.pyf --quiet``. This
      generates ``mymodmodule.c`` and (if needed)
      ``mymod-f2pywrappers.f`` files next to ``mymod.pyf``.
    * Step 2: build your Python extension module. This requires the
      following source files:

      * ``mymodmodule.c``
      * ``mymod-f2pywrappers.f`` (if it was generated in Step 1)
      * ``fortranobject.c``

    See Also
    --------
    numpy.get_include : function that returns the numpy include directory

    """
    return os.path.join(os.path.dirname(__file__), 'src')


def get_include():
    """
    Return the directory that contains the NumPy \\*.h header files.

    Extension modules that need to compile against NumPy may need to use this
    function to locate the appropriate include directory.

    Notes
    -----
    When using ``setuptools``, for example in ``setup.py``::

        import numpy as np
        ...
        Extension('extension_name', ...
                  include_dirs=[np.get_include()])
        ...

    Note that a CLI tool ``numpy-config`` was introduced in NumPy 2.0, using
    that is likely preferred for build systems other than ``setuptools``::

        $ numpy-config --cflags
        -I/path/to/site-packages/numpy/_core/include

        # Or rely on pkg-config:
        $ export PKG_CONFIG_PATH=$(numpy-config --pkgconfigdir)
        $ pkg-config --cflags
        -I/path/to/site-packages/numpy/_core/include

    Examples
    --------
    >>> np.get_include()
    '.../site-packages/numpy/core/include'  # may vary

    """
    import numpy
    if numpy.show_config is None:
        # running from numpy source directory
        d = os.path.join(os.path.dirname(numpy.__file__), '_core', 'include')
    else:
        # using installed numpy core headers
        import numpy._core as _core
        d = os.path.join(os.path.dirname(_core.__file__), 'include')
    return d

