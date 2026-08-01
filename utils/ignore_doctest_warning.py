
def ignore_doctest_warning(item: pytest.Item, path: str, message: str) -> None:
    """Ignore doctest warning.

    Parameters
    ----------
    item : pytest.Item
        pytest test item.
    path : str
        Module path to Python object, e.g. "pandas.DataFrame.append". A
        warning will be filtered when item.name ends with in given path. So it is
        sufficient to specify e.g. "DataFrame.append".
    message : str
        Message to be filtered.
    """
    if item.name.endswith(path):
        item.add_marker(pytest.mark.filterwarnings(f"ignore:{message}"))

