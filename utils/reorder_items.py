
def reorder_items(items: Sequence[nodes.Item]) -> list[nodes.Item]:
    argkeys_by_item: dict[Scope, dict[nodes.Item, OrderedSet[ParamArgKey]]] = {}
    items_by_argkey: dict[Scope, dict[ParamArgKey, OrderedDict[nodes.Item, None]]] = {}
    for scope in HIGH_SCOPES:
        scoped_argkeys_by_item = argkeys_by_item[scope] = {}
        scoped_items_by_argkey = items_by_argkey[scope] = defaultdict(OrderedDict)
        for item in items:
            argkeys = dict.fromkeys(get_param_argkeys(item, scope))
            if argkeys:
                scoped_argkeys_by_item[item] = argkeys
                for argkey in argkeys:
                    scoped_items_by_argkey[argkey][item] = None

    items_set = dict.fromkeys(items)
    return list(
        reorder_items_atscope(
            items_set, argkeys_by_item, items_by_argkey, Scope.Session
        )
    )

