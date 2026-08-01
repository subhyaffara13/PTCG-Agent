
def package_wheel_requirement_url(
    pylock_path_or_url: str, package_wheel: PackageWheel
) -> str:
    return _package_dist_url(pylock_path_or_url, package_wheel.path, package_wheel.url)

