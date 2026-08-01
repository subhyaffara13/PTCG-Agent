
def get_dataset_names():
    """Report available example datasets, useful for reporting issues.

    Requires an internet connection.

    """
    with urlopen(DATASET_NAMES_URL) as resp:
        txt = resp.read()

    dataset_names = [name.strip() for name in txt.decode().split("\n")]
    return list(filter(None, dataset_names))

