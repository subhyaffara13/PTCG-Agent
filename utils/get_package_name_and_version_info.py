
def get_package_name_and_version_info():
    package_name = ""
    version = ""
    cuda_version = ""

    try:
        from .build_and_package_info import __version__ as version  # noqa: PLC0415
        from .build_and_package_info import package_name  # noqa: PLC0415

        try:  # noqa: SIM105
            from .build_and_package_info import cuda_version  # noqa: PLC0415
        except ImportError:
            # cuda_version is optional. For example, cpu only package does not have the attribute.
            pass
    except Exception as e:
        warnings.warn("WARNING: failed to collect package name and version info")
        print(e)

    return package_name, version, cuda_version

