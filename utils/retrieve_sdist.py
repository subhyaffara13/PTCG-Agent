import os

def retrieve_sdist(package, version, tmp_path):
    """Either use cached sdist file or download it from PyPI"""
    # `pip download` cannot be used due to
    # https://github.com/pypa/pip/issues/1884
    # https://discuss.python.org/t/pep-625-file-name-of-a-source-distribution/4686
    # We have to find the correct distribution file and download it
    download_path = os.getenv("DOWNLOAD_PATH", str(tmp_path))
    dist = retrieve_pypi_sdist_metadata(package, version)

    # Remove old files to prevent cache to grow indefinitely
    for file in glob(os.path.join(download_path, f"{package}*")):
        if dist["filename"] != file:
            os.unlink(file)

    dist_file = os.path.join(download_path, dist["filename"])
    if not os.path.exists(dist_file):
        download(dist["url"], dist_file, dist["md5_digest"])
    return dist_file

