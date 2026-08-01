
def _compute_upgrade_prompt(
    local_version: Version, remote_version_str: str, installed_by_pip: bool
) -> UpgradePrompt | None:
    remote_version = parse_version(remote_version_str)
    logger.debug("Remote version of pip: %s", remote_version)
    logger.debug("Local version of pip:  %s", local_version)
    logger.debug("Was pip installed by pip? %s", installed_by_pip)

    if not installed_by_pip:
        return None  # Only suggest upgrade if pip is installed by pip.

    local_version_is_older = (
        local_version < remote_version
        and local_version.base_version != remote_version.base_version
    )
    if local_version_is_older:
        return UpgradePrompt(old=str(local_version), new=remote_version_str)

    return None

