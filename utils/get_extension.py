import os
import sys

def get_extension(srcfilename, modname, sources=(), **kwds):
    from cffi._shimmed_dist_utils import Extension
    allsources = [srcfilename]
    for src in sources:
        allsources.append(os.path.normpath(src))
    return Extension(name=modname, sources=allsources, **kwds)


def get_extension() -> type[Extension]:
    # We can work with either setuptools or distutils, and pick setuptools
    # if it has been imported.
    use_setuptools = "setuptools" in sys.modules
    extension_class: type[Extension]

    if sys.version_info < (3, 12) and not use_setuptools:
        import distutils.core

        extension_class = distutils.core.Extension
    else:
        if not use_setuptools:
            sys.exit("error: setuptools not installed")
        extension_class = setuptools.Extension

    return extension_class

