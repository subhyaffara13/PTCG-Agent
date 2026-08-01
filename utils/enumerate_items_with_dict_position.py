
def enumerate_items_with_dict_position(
    obj: dict[K, V],
) -> Iterable[tuple[int, K, V | Any]]:
    """Enumerate dict items yielding (dict_keys_position, key, value).

    For OrderedDicts where move_to_end/prepend has been used, the OrderedDict
    iteration order can differ from dict.keys() order.  We iterate in
    OrderedDict order (correct execution semantics) but return each key's
    dict.keys() position so that ConstDictKeySource indices stay consistent
    with PyDict_Next / C++ DictGuardManager.
    """
    items = get_items_from_dict(obj)
    if isinstance(obj, OrderedDict):
        key_to_pos = {k: i for i, k in enumerate(dict.keys(obj))}
        return ((key_to_pos[k], k, v) for k, v in items)
    return ((i, k, v) for i, (k, v) in enumerate(items))

