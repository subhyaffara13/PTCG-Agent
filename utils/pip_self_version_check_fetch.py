
def pip_self_version_check_fetch(
    session: PipSession, options: optparse.Values
) -> UpgradePrompt | None:
    """Compute the pip upgrade prompt, if any, before the command runs.

    Limit the frequency of checks to once per week. State is stored either in
    the active virtualenv or in the user's USER_CACHE_DIR keyed off the prefix
    of the pip script path.

    Pair with :func:`pip_self_version_check_emit`, which displays the prompt
    after the command body runs.
    """
    installed_dist = get_default_environment().get_distribution("pip")
    if not installed_dist:
        return None
    try:
        check_externally_managed()
    except ExternallyManagedEnvironment:
        return None

    state = SelfCheckState(cache_dir=options.cache_dir)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    remote_version_str = state.get(current_time)
    if remote_version_str is None:
        remote_version_str = _get_current_remote_pip_version(session, options)
        if remote_version_str is None:
            logger.debug("No remote pip version found")
            return None
        state.set(remote_version_str, current_time)

    return _compute_upgrade_prompt(
        local_version=installed_dist.version,
        remote_version_str=remote_version_str,
        installed_by_pip=installed_dist.installer == "pip",
    )

