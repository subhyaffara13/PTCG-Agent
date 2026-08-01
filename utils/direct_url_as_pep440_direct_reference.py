
def direct_url_as_pep440_direct_reference(direct_url: DirectUrl, name: str) -> str:
    """Convert a DirectUrl to a pip requirement string."""
    direct_url.validate()  # if invalid, this is a pip bug
    requirement = name + " @ "
    fragments = []
    if direct_url.vcs_info:
        requirement += (
            f"{direct_url.vcs_info.vcs}+{direct_url.url}"
            f"@{direct_url.vcs_info.commit_id}"
        )
    elif direct_url.archive_info:
        requirement += direct_url.url
        if direct_url.archive_info.hashes:
            hash_algorithm, hash_value = next(
                iter(direct_url.archive_info.hashes.items())
            )
            fragments.append(f"{hash_algorithm}={hash_value}")
    else:
        assert direct_url.dir_info
        requirement += direct_url.url
    if direct_url.subdirectory:
        fragments.append("subdirectory=" + direct_url.subdirectory)
    if fragments:
        requirement += "#" + "&".join(fragments)
    return requirement

