
def download_all(path=None):
    """
    Utility method to download all the dataset files
    for `scipy.datasets` module.

    Parameters
    ----------
    path : str, optional
        Directory path to download all the dataset files.
        If None, default to the system cache_dir detected by pooch.

    Examples
    --------
    Download the datasets to the default cache location:

    >>> from scipy import datasets
    >>> datasets.download_all()

    Download the datasets to the current directory:

    >>> datasets.download_all(".")

    """
    if pooch is None:
        raise ImportError("Missing optional dependency 'pooch' required "
                          "for scipy.datasets module. Please use pip or "
                          "conda to install 'pooch'.")
    if path is None:
        path = pooch.os_cache('scipy-data')
    # https://github.com/scipy/scipy/issues/21879
    downloader = pooch.HTTPDownloader(headers={"User-Agent": "SciPy"})
    for dataset_name, dataset_hash in _registry.registry.items():
        pooch.retrieve(url=_registry.registry_urls[dataset_name],
                       known_hash=dataset_hash,
                       fname=dataset_name, path=path, downloader=downloader)

