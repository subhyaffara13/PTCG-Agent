import os

def help(github, model, force_reload=False, skip_validation=False, trust_repo="check"):
    r"""
    Show the docstring of entrypoint ``model``.

    Args:
        github (str): a string with format <repo_owner/repo_name[:ref]> with an optional
            ref (a tag or a branch). If ``ref`` is not specified, the default branch is assumed
            to be ``main`` if it exists, and otherwise ``master``.
            Example: 'pytorch/vision:0.10'
        model (str): a string of entrypoint name defined in repo's ``hubconf.py``
        force_reload (bool, optional): whether to discard the existing cache and force a fresh download.
            Default is ``False``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the ref
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
        trust_repo (bool or str): ``"check"``, ``True`` or ``False``.
            This parameter was introduced in v1.12 and helps ensuring that users
            only run code from repos that they trust.

            - If ``False``, a prompt will ask the user whether the repo should
              be trusted.
            - If ``True``, the repo will be added to the trusted list and loaded
              without requiring explicit confirmation.
            - If ``"check"``, the repo will be checked against the list of
              trusted repos in the cache. If it is not present in that list, the
              behaviour will fall back onto the ``trust_repo=False`` option.

            Default is ``"check"``.
    Example:
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_HUB)
        >>> print(torch.hub.help("pytorch/vision", "resnet18", force_reload=True))
    """
    repo_dir = _get_cache_or_reload(
        github,
        force_reload,
        trust_repo,
        verbose=True,
        skip_validation=skip_validation,
    )

    with _add_to_sys_path(repo_dir):
        hubconf_path = os.path.join(repo_dir, MODULE_HUBCONF)
        hub_module = _import_module(MODULE_HUBCONF, hubconf_path)

    entry = _load_entry_from_hubconf(hub_module, model)

    return entry.__doc__

