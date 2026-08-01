
def strict_data_files(pytestconfig):
    """
    Returns the configuration for the test setting `--no-strict-data-files`.
    """
    return pytestconfig.getoption("--no-strict-data-files")

