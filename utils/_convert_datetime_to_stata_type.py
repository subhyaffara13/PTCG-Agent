
def _convert_datetime_to_stata_type(fmt: str) -> np.dtype:
    """
    Convert from one of the stata date formats to a type in TYPE_MAP.
    """
    if fmt in [
        "tc",
        "%tc",
        "td",
        "%td",
        "tw",
        "%tw",
        "tm",
        "%tm",
        "tq",
        "%tq",
        "th",
        "%th",
        "ty",
        "%ty",
    ]:
        return np.dtype(np.float64)  # Stata expects doubles for SIFs
    else:
        raise NotImplementedError(f"Format {fmt} not implemented")

