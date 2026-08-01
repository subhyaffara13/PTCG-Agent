
def package_archive_requirement_url(
    pylock_path_or_url: str, package_archive: PackageArchive
) -> str:
    url = _package_dist_url(
        pylock_path_or_url, package_archive.path, package_archive.url
    )
    if package_archive.subdirectory:
        if "#" in url:
            raise InstallationError(
                f"Package URL {url!r} cannot contain fragments in combination "
                f"with subdirectory field (in {pylock_path_or_url!r})"
            )
        url += "#subdirectory=" + package_archive.subdirectory
    return url

