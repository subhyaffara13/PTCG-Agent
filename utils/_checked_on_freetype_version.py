
def _checked_on_freetype_version(required_freetype_version):
    import pytest
    return pytest.mark.xfail(
        not _check_freetype_version(required_freetype_version),
        reason=f"Mismatched version of freetype. "
               f"Test requires '{required_freetype_version}', "
               f"you have '{ft2font.__freetype_version__}'",
        raises=ImageComparisonFailure, strict=False)

