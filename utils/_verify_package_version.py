
def _verify_package_version(version: str) -> None:
    # Occasionally we run into situations where the version of the Python
    # package does not match the version of the shared object that is loaded.
    # This may occur in environments where multiple versions of cryptography
    # are installed and available in the python path. To avoid errors cropping
    # up later this code checks that the currently imported package and the
    # shared object that were loaded have the same version and raise an
    # ImportError if they do not
    so_package_version = _openssl.ffi.string(
        _openssl.lib.CRYPTOGRAPHY_PACKAGE_VERSION
    )
    if version.encode("ascii") != so_package_version:
        raise ImportError(
            "The version of cryptography does not match the loaded "
            "shared object. This can happen if you have multiple copies of "
            "cryptography installed in your Python path. Please try creating "
            "a new virtual environment to resolve this issue. "
            f"Loaded python version: {version}, "
            f"shared object version: {so_package_version}"
        )

    _openssl_assert(
        _openssl.lib.OpenSSL_version_num() == openssl.openssl_version(),
    )

