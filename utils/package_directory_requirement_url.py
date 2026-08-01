
def package_directory_requirement_url(
    pylock_path_or_url: str, package_directory: PackageDirectory
) -> str:
    if _is_url(pylock_path_or_url) and not pylock_path_or_url.startswith("file://"):
        raise InstallationError(
            f"Directory entries are not supported in remote pylock.toml "
            f"{pylock_path_or_url!r}"
        )
    url = _package_dist_url(pylock_path_or_url, package_directory.path, None)
    assert url.startswith("file://")
    if not url.endswith("/"):
        url += "/"
    if package_directory.subdirectory:
        url += package_directory.subdirectory
        if not url.endswith("/"):
            url += "/"
    return url

