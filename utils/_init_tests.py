
def _init_tests():
    # The version of FreeType to install locally for running the tests. This must match
    # the value in `subprojects/freetype2.wrap`.
    LOCAL_FREETYPE_VERSION = '2.14.3'

    from matplotlib import ft2font
    if (ft2font.__freetype_version__ != LOCAL_FREETYPE_VERSION or
            ft2font.__freetype_build_type__ != 'local'):
        _log.warning(
            "Matplotlib is not built with the correct FreeType version to run tests.  "
            "Rebuild without setting system-freetype=true in Meson setup options.  "
            "Expect many image comparison failures below.  "
            "Expected freetype version %s.  "
            "Found freetype version %s.  "
            "Freetype build type is %slocal.",
            LOCAL_FREETYPE_VERSION,
            ft2font.__freetype_version__,
            "" if ft2font.__freetype_build_type__ == 'local' else "not ")

    # Generate a shortcut for classic testing style.
    from matplotlib.style import _base_library, library
    _base_library['_classic_test'] = library['_classic_test'] = RcParams(
            _base_library['classic'] | _base_library['_classic_test_patch'])

