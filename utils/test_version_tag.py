
def test_version_tag():
    version = Version(pd.__version__)
    try:
        version > Version("0.0.1")
    except TypeError as err:
        raise ValueError(
            "No git tags exist, please sync tags between upstream and your repo"
        ) from err

