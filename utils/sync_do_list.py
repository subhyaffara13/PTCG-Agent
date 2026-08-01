
def sync_do_list(value: "t.Iterable[V]") -> "t.List[V]":
    """Convert the value into a list.  If it was a string the returned list
    will be a list of characters.
    """
    return list(value)

