
def install_req_from_pylock_package(
    package: pylock.Package,
    package_dist: (
        pylock.PackageVcs
        | pylock.PackageArchive
        | pylock.PackageDirectory
        | pylock.PackageSdist
        | pylock.PackageWheel
    ),
    pylock_path_or_url: str,
    format_control: FormatControl,
    user_supplied: bool,
) -> InstallRequirement:
    pass
    # TODO: validate file size
    if isinstance(package_dist, pylock.PackageVcs):
        return InstallRequirement(
            req=Requirement(
                f"{package.name} @ "
                f"{package_vcs_requirement_url(pylock_path_or_url, package_dist)}"
            ),
            comes_from=pylock_path_or_url,
            user_supplied=user_supplied,
        )
    elif isinstance(package_dist, pylock.PackageArchive):
        return InstallRequirement(
            req=Requirement(
                f"{package.name} @ "
                f"{package_archive_requirement_url(pylock_path_or_url, package_dist)}"
            ),
            comes_from=pylock_path_or_url,
            hash_options=_pylock_hashes_to_hash_options(package_dist.hashes),
            user_supplied=user_supplied,
        )
    elif isinstance(package_dist, pylock.PackageDirectory):
        req = package_directory_requirement_url(pylock_path_or_url, package_dist)
        if package_dist.editable:
            return install_req_from_editable(
                req,
                comes_from=pylock_path_or_url,
                user_supplied=user_supplied,
            )
        else:
            return install_req_from_line(
                req,
                comes_from=pylock_path_or_url,
                user_supplied=user_supplied,
            )
    else:
        # wheel or sdist
        allowed_formats = format_control.get_allowed_formats(package.name)
        if (
            isinstance(package_dist, pylock.PackageSdist)
            and "source" not in allowed_formats
        ):
            raise InstallationError(
                f"source distributions are not permitted for package {package.name!r} "
                f"and there is no compatible wheel for it in {pylock_path_or_url!r}"
            )
        if (
            isinstance(package_dist, pylock.PackageWheel)
            and "binary" not in allowed_formats
        ):
            if not package.sdist:
                raise InstallationError(
                    f"binaries are not permitted for package {package.name!r} and "
                    f"there is no source distribution for it in {pylock_path_or_url!r}"
                )
            package_dist = package.sdist
        version = package.version
        if isinstance(package_dist, pylock.PackageWheel):
            if not version:
                _, version, _, _ = parse_wheel_filename(package_dist.filename)
            requirement_url = package_wheel_requirement_url(
                pylock_path_or_url, package_dist
            )
        elif isinstance(package_dist, pylock.PackageSdist):
            if not version:
                _, version = parse_sdist_filename(package_dist.filename)
            requirement_url = package_sdist_requirement_url(
                pylock_path_or_url, package_dist
            )
        ireq = InstallRequirement(
            req=Requirement(f"{package.name}=={version}"),
            comes_from=pylock_path_or_url,
            locked_link=Link(requirement_url),
            locked_version=version,
            hash_options=_pylock_hashes_to_hash_options(package_dist.hashes),
            user_supplied=user_supplied,
        )
        return ireq

