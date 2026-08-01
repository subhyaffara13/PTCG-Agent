
def fetch_data(dataset_name, data_fetcher=data_fetcher):
    if data_fetcher is None:
        raise ImportError("Missing optional dependency 'pooch' required "
                          "for scipy.datasets module. Please use pip or "
                          "conda to install 'pooch'.")
    # https://github.com/scipy/scipy/issues/21879
    downloader = pooch.HTTPDownloader(
        headers={"User-Agent": f"SciPy {sys.modules['scipy'].__version__}"}
    )
    # The "fetch" method returns the full path to the downloaded data file.
    return data_fetcher.fetch(dataset_name, downloader=downloader)

