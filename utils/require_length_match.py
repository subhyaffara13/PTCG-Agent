
def require_length_match(data, index: Index) -> None:
    """
    Check the length of data matches the length of the index.
    """
    if len(data) != len(index):
        raise ValueError(
            "Length of values "
            f"({len(data)}) "
            "does not match length of index "
            f"({len(index)})"
        )

