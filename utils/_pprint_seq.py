
def _pprint_seq(
    seq: ListLike, _nest_lvl: int = 0, max_seq_items: int | None = None, **kwds: Any
) -> str:
    """
    internal. pprinter for iterables. you should probably use pprint_thing()
    rather than calling this directly.

    bounds length of printed sequence, depending on options
    """
    if isinstance(seq, set):
        fmt = "{{{body}}}"
    elif isinstance(seq, frozenset):
        fmt = "frozenset({{{body}}})"
    else:
        fmt = "[{body}]" if hasattr(seq, "__setitem__") else "({body})"

    if max_seq_items is False:
        max_items = None
    else:
        max_items = max_seq_items or get_option("max_seq_items") or len(seq)

    s = iter(seq)
    # handle sets, no slicing
    r = []
    max_items_reached = False
    for i, item in enumerate(s):
        if (max_items is not None) and (i >= max_items):
            max_items_reached = True
            break
        r.append(pprint_thing(item, _nest_lvl + 1, max_seq_items=max_seq_items, **kwds))
    body = ", ".join(r)

    if max_items_reached:
        body += ", ..."
    elif isinstance(seq, tuple) and len(seq) == 1:
        body += ","

    return fmt.format(body=body)

