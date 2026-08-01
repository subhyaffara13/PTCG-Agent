
def package_vcs_requirement_url(
    pylock_path_or_url: str, package_vcs: PackageVcs
) -> str:
    dist_url = _package_dist_url(pylock_path_or_url, package_vcs.path, package_vcs.url)
    url = f"{package_vcs.type}+{dist_url}@{package_vcs.commit_id}"
    if package_vcs.subdirectory:
        if "#" in url:
            raise InstallationError(
                f"Package URL {url!r} cannot contain fragments in combination "
                f"with subdirectory field (in {pylock_path_or_url!r})"
            )
        url += "#subdirectory=" + package_vcs.subdirectory
    return url

