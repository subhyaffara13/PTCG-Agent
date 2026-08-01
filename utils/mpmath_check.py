
def mpmath_check(min_ver):
    return pytest.mark.skipif(
        mpmath is None
        or version.parse(mpmath.__version__) < version.Version(min_ver),
        reason=f"mpmath version >= {min_ver} required",
    )

