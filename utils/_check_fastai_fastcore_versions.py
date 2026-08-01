
def _check_fastai_fastcore_versions(
    fastai_min_version: str = "2.4",
    fastcore_min_version: str = "1.3.27",
):
    """
    Checks that the installed fastai and fastcore versions are compatible for pickle serialization.

    Args:
        fastai_min_version (`str`, *optional*):
            The minimum fastai version supported.
        fastcore_min_version (`str`, *optional*):
            The minimum fastcore version supported.

    > [!TIP]
    > Raises the following error:
    >
    >     - [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
    >       if the fastai or fastcore libraries are not available or are of an invalid version.
    """

    if (get_fastcore_version() or get_fastai_version()) == "N/A":
        raise ImportError(
            f"fastai>={fastai_min_version} and fastcore>={fastcore_min_version} are"
            f" required. Currently using fastai=={get_fastai_version()} and"
            f" fastcore=={get_fastcore_version()}."
        )

    current_fastai_version = version.Version(get_fastai_version())
    current_fastcore_version = version.Version(get_fastcore_version())

    if current_fastai_version < version.Version(fastai_min_version):
        raise ImportError(
            "`push_to_hub_fastai` and `from_pretrained_fastai` require a"
            f" fastai>={fastai_min_version} version, but you are using fastai version"
            f" {get_fastai_version()} which is incompatible. Upgrade with `pip install"
            " fastai==2.5.6`."
        )

    if current_fastcore_version < version.Version(fastcore_min_version):
        raise ImportError(
            "`push_to_hub_fastai` and `from_pretrained_fastai` require a"
            f" fastcore>={fastcore_min_version} version, but you are using fastcore"
            f" version {get_fastcore_version()} which is incompatible. Upgrade with"
            " `pip install fastcore==1.3.27`."
        )

