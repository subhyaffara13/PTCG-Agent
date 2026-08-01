
def _download(url, filename, directory="/tmp/mnist"):
    """Download a url to a file in the given directory."""
    if not path.exists(directory):
        os.makedirs(directory)
    out_file = path.join(directory, filename)
    if not path.isfile(out_file):
        urlretrieve(url, out_file)
        logging.info("Downloaded %s to %s", url, directory)

