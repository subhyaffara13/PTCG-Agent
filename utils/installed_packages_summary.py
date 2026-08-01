
def installed_packages_summary(
    installed: list[InstallationResult], env: BaseEnvironment
) -> str:
    # Format a summary of installed packages, with extra care to
    # display a package name as it was requested by the user.
    installed.sort(key=operator.attrgetter("name"))
    summary = []
    installed_versions = {}
    for distribution in env.iter_all_distributions():
        installed_versions[distribution.canonical_name] = distribution.version
    for package in installed:
        display_name = package.name
        version = installed_versions.get(canonicalize_name(display_name), None)
        if version:
            text = f"{display_name}-{version}"
        else:
            text = display_name
        summary.append(text)

    if not summary:
        return ""
    return f"Successfully installed {' '.join(summary)}"

