import os

def _check_fastai_fastcore_pyproject_versions(
    storage_folder: str,
    fastai_min_version: str = "2.4",
    fastcore_min_version: str = "1.3.27",
):
    """
    Checks that the `pyproject.toml` file in the directory `storage_folder` has fastai and fastcore versions
    that are compatible with `from_pretrained_fastai` and `push_to_hub_fastai`. If `pyproject.toml` does not exist
    or does not contain versions for fastai and fastcore, then it logs a warning.

    Args:
        storage_folder (`str`):
            Folder to look for the `pyproject.toml` file.
        fastai_min_version (`str`, *optional*):
            The minimum fastai version supported.
        fastcore_min_version (`str`, *optional*):
            The minimum fastcore version supported.

    > [!TIP]
    > Raises the following errors:
    >
    >     - [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
    >       if the `toml` module is not installed.
    >     - [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
    >       if the `pyproject.toml` indicates a lower than minimum supported version of fastai or fastcore.
    """

    try:
        import toml
    except ModuleNotFoundError:
        raise ImportError(
            "`push_to_hub_fastai` and `from_pretrained_fastai` require the toml module."
            " Install it with `pip install toml`."
        )

    # Checks that a `pyproject.toml`, with `build-system` and `requires` sections, exists in the repository. If so, get a list of required packages.
    if not os.path.isfile(f"{storage_folder}/pyproject.toml"):
        logger.warning(
            "There is no `pyproject.toml` in the repository that contains the fastai"
            " `Learner`. The `pyproject.toml` would allow us to verify that your fastai"
            " and fastcore versions are compatible with those of the model you want to"
            " load."
        )
        return
    pyproject_toml = toml.load(f"{storage_folder}/pyproject.toml")

    if "build-system" not in pyproject_toml.keys():
        logger.warning(
            "There is no `build-system` section in the pyproject.toml of the repository"
            " that contains the fastai `Learner`. The `build-system` would allow us to"
            " verify that your fastai and fastcore versions are compatible with those"
            " of the model you want to load."
        )
        return
    build_system_toml = pyproject_toml["build-system"]

    if "requires" not in build_system_toml.keys():
        logger.warning(
            "There is no `requires` section in the pyproject.toml of the repository"
            " that contains the fastai `Learner`. The `requires` would allow us to"
            " verify that your fastai and fastcore versions are compatible with those"
            " of the model you want to load."
        )
        return
    package_versions = build_system_toml["requires"]

    # Extracts contains fastai and fastcore versions from `pyproject.toml` if available.
    # If the package is specified but not the version (e.g. "fastai" instead of "fastai=2.4"), the default versions are the highest.
    fastai_packages = [pck for pck in package_versions if pck.startswith("fastai")]
    if len(fastai_packages) == 0:
        logger.warning("The repository does not have a fastai version specified in the `pyproject.toml`.")
    # fastai_version is an empty string if not specified
    else:
        fastai_version = str(fastai_packages[0]).partition("=")[2]
        if fastai_version != "" and version.Version(fastai_version) < version.Version(fastai_min_version):
            raise ImportError(
                "`from_pretrained_fastai` requires"
                f" fastai>={fastai_min_version} version but the model to load uses"
                f" {fastai_version} which is incompatible."
            )

    fastcore_packages = [pck for pck in package_versions if pck.startswith("fastcore")]
    if len(fastcore_packages) == 0:
        logger.warning("The repository does not have a fastcore version specified in the `pyproject.toml`.")
    # fastcore_version is an empty string if not specified
    else:
        fastcore_version = str(fastcore_packages[0]).partition("=")[2]
        if fastcore_version != "" and version.Version(fastcore_version) < version.Version(fastcore_min_version):
            raise ImportError(
                "`from_pretrained_fastai` requires"
                f" fastcore>={fastcore_min_version} version, but you are using fastcore"
                f" version {fastcore_version} which is incompatible."
            )

