
def test_limited_api(install_temp):
    """Test building a third-party C extension with the limited API
    and building a cython extension with the limited API
    """

    import limited_api1  # Earliest (3.6)  # noqa: F401
    import limited_api2  # cython  # noqa: F401
    import limited_api_latest  # Latest version (current Python)  # noqa: F401

