import sys

def reorder_items_atscope(
    items: OrderedSet[nodes.Item],
    argkeys_by_item: Mapping[Scope, Mapping[nodes.Item, OrderedSet[ParamArgKey]]],
    items_by_argkey: Mapping[
        Scope, Mapping[ParamArgKey, OrderedDict[nodes.Item, None]]
    ],
    scope: Scope,
) -> OrderedSet[nodes.Item]:
    if scope is Scope.Function or len(items) < 3:
        return items

    scoped_items_by_argkey = items_by_argkey[scope]
    scoped_argkeys_by_item = argkeys_by_item[scope]

    ignore: set[ParamArgKey] = set()
    items_deque = deque(items)
    items_done: OrderedSet[nodes.Item] = {}
    while items_deque:
        no_argkey_items: OrderedSet[nodes.Item] = {}
        slicing_argkey = None
        while items_deque:
            item = items_deque.popleft()
            if item in items_done or item in no_argkey_items:
                continue
            argkeys = dict.fromkeys(
                k for k in scoped_argkeys_by_item.get(item, ()) if k not in ignore
            )
            if not argkeys:
                no_argkey_items[item] = None
            else:
                slicing_argkey, _ = argkeys.popitem()
                # We don't have to remove relevant items from later in the
                # deque because they'll just be ignored.
                matching_items = [
                    i for i in scoped_items_by_argkey[slicing_argkey] if i in items
                ]
                for i in reversed(matching_items):
                    items_deque.appendleft(i)
                    # Fix items_by_argkey order.
                    for other_scope in HIGH_SCOPES:
                        other_scoped_items_by_argkey = items_by_argkey[other_scope]
                        for argkey in argkeys_by_item[other_scope].get(i, ()):
                            argkey_dict = other_scoped_items_by_argkey[argkey]
                            if not hasattr(sys, "pypy_version_info"):
                                argkey_dict[i] = None
                                argkey_dict.move_to_end(i, last=False)
                            else:
                                # Work around a bug in PyPy:
                                # https://github.com/pypy/pypy/issues/5257
                                # https://github.com/pytest-dev/pytest/issues/13312
                                bkp = argkey_dict.copy()
                                argkey_dict.clear()
                                argkey_dict[i] = None
                                argkey_dict.update(bkp)
                break
        if no_argkey_items:
            reordered_no_argkey_items = reorder_items_atscope(
                no_argkey_items, argkeys_by_item, items_by_argkey, scope.next_lower()
            )
            items_done.update(reordered_no_argkey_items)
        if slicing_argkey is not None:
            ignore.add(slicing_argkey)
    return items_done

