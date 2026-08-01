
def install_given_reqs(
    requirements: list[InstallRequirement],
    root: str | None,
    home: str | None,
    prefix: str | None,
    warn_script_location: bool,
    use_user_site: bool,
    pycompile: bool,
    progress_bar: BarType,
) -> list[InstallationResult]:
    """
    Install everything in the given list.

    (to be called after having downloaded and unpacked the packages)
    """
    to_install = collections.OrderedDict(_validate_requirements(requirements))

    if to_install:
        logger.info(
            "Installing collected packages: %s",
            ", ".join(to_install.keys()),
        )

    installed = []

    show_progress = logger.isEnabledFor(logging.INFO) and len(to_install) > 1

    items = iter(to_install.values())
    if show_progress:
        renderer = get_install_progress_renderer(
            bar_type=progress_bar, total=len(to_install)
        )
        items = renderer(items)

    with indent_log():
        for requirement in items:
            req_name = requirement.name
            assert req_name is not None
            if requirement.should_reinstall:
                logger.info("Attempting uninstall: %s", req_name)
                with indent_log():
                    uninstalled_pathset = requirement.uninstall(auto_confirm=True)
            else:
                uninstalled_pathset = None

            try:
                requirement.install(
                    root=root,
                    home=home,
                    prefix=prefix,
                    warn_script_location=warn_script_location,
                    use_user_site=use_user_site,
                    pycompile=pycompile,
                )
            except Exception:
                # if install did not succeed, rollback previous uninstall
                if uninstalled_pathset and not requirement.install_succeeded:
                    uninstalled_pathset.rollback()
                raise
            else:
                if uninstalled_pathset and requirement.install_succeeded:
                    uninstalled_pathset.commit()

            installed.append(InstallationResult(req_name))

    return installed

