
def package_sdist_requirement_url(
    pylock_path_or_url: str, package_sdist: PackageSdist
) -> str:
    return _package_dist_url(pylock_path_or_url, package_sdist.path, package_sdist.url)

