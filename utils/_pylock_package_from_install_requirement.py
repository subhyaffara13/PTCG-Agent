from pathlib import Path


def _pylock_package_from_install_requirement(
    ireq: InstallRequirement, base_dir: Path
) -> Package:
    base_dir = base_dir.resolve()
    dist = ireq.get_dist()
    download_info = ireq.download_info
    assert download_info
    package_version = None
    package_vcs = None
    package_directory = None
    package_archive = None
    package_sdist = None
    package_wheels = None
    if ireq.is_direct:
        if download_info.vcs_info:
            package_vcs = PackageVcs(
                type=download_info.vcs_info.vcs,
                url=download_info.url,
                path=None,
                requested_revision=download_info.vcs_info.requested_revision,
                commit_id=download_info.vcs_info.commit_id,
                subdirectory=download_info.subdirectory,
            )
        elif download_info.dir_info:
            package_directory = PackageDirectory(
                path=(
                    Path(url_to_path(download_info.url))
                    .resolve()
                    .relative_to(base_dir)
                    .as_posix()
                ),
                editable=(
                    download_info.dir_info.editable
                    if download_info.dir_info.editable
                    else None
                ),
                subdirectory=download_info.subdirectory,
            )
        elif download_info.archive_info:
            if not download_info.archive_info.hashes:
                raise NotImplementedError()
            package_archive = PackageArchive(
                url=download_info.url,
                path=None,
                hashes=download_info.archive_info.hashes,
                subdirectory=download_info.subdirectory,
            )
        else:
            # should never happen
            raise NotImplementedError()
    else:
        package_version = dist.version
        if download_info.archive_info:
            if not download_info.archive_info.hashes:
                raise NotImplementedError()
            link = Link(download_info.url)
            if link.is_wheel:
                package_wheels = [
                    PackageWheel(
                        name=link.filename,
                        url=download_info.url,
                        hashes=download_info.archive_info.hashes,
                    )
                ]
            else:
                package_sdist = PackageSdist(
                    name=link.filename,
                    url=download_info.url,
                    hashes=download_info.archive_info.hashes,
                )
        else:
            # should never happen
            raise NotImplementedError()
    return Package(
        name=dist.canonical_name,
        version=package_version,
        vcs=package_vcs,
        directory=package_directory,
        archive=package_archive,
        sdist=package_sdist,
        wheels=package_wheels,
    )

