from pathlib import Path


def get_data_path():
    """Return the path to Matplotlib data."""
    return str(Path(__file__).with_name("mpl-data"))

