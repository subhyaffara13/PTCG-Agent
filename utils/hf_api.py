
def hf_api() -> HfApi:
    """Return a shared HfApi instance tagged with transformers's library info.

    Routing Hub calls (create_repo, create_commit, snapshot_download, ...) through this
    instance ensures the library_name/library_version are reported consistently to the Hub.
    """
    global _hf_api
    if _hf_api is None:
        _hf_api = HfApi(
            library_name="transformers",
            library_version=__version__,
        )
    return _hf_api

