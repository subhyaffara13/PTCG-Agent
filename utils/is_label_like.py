
def is_label_like(key) -> bool:
    """
    Returns
    -------
    bool
    """
    # select a label or row
    return (
        not isinstance(key, slice)
        and not is_list_like_indexer(key)
        and key is not Ellipsis
    )

