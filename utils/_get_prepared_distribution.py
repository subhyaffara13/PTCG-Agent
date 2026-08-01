
def _get_prepared_distribution(
    req: InstallRequirement,
    build_tracker: BuildTracker,
    build_env_installer: BuildEnvironmentInstaller,
    build_isolation: bool,
    check_build_deps: bool,
) -> BaseDistribution:
    """Prepare a distribution for installation."""
    abstract_dist = make_distribution_for_install_requirement(req)
    tracker_id = abstract_dist.build_tracker_id
    if tracker_id is not None:
        with build_tracker.track(req, tracker_id):
            abstract_dist.prepare_distribution_metadata(
                build_env_installer, build_isolation, check_build_deps
            )
    return abstract_dist.get_metadata_distribution()

