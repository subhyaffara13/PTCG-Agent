
def check_warnings_filter() -> bool:
    """Return True if any other than the default DeprecationWarning filter is enabled.

    https://docs.python.org/3/library/warnings.html#default-warning-filter
    """
    return any(
        issubclass(DeprecationWarning, filter[2])
        and filter[0] != "ignore"
        and filter[3] != "__main__"
        for filter in warnings.filters
    )

