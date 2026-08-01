
def get_param_argkeys(item: nodes.Item, scope: Scope) -> Iterator[ParamArgKey]:
    """Return all ParamArgKeys for item matching the specified high scope."""
    assert scope is not Scope.Function

    try:
        callspec: CallSpec2 = item.callspec  # type: ignore[attr-defined]
    except AttributeError:
        return

    item_cls = None
    if scope is Scope.Session:
        scoped_item_path = None
    elif scope is Scope.Package:
        # Package key = module's directory.
        scoped_item_path = item.path.parent
    elif scope is Scope.Module:
        scoped_item_path = item.path
    elif scope is Scope.Class:
        scoped_item_path = item.path
        item_cls = item.cls  # type: ignore[attr-defined]
    else:
        assert_never(scope)

    for argname in callspec.indices:
        if callspec._arg2scope[argname] != scope:
            continue
        param_index = callspec.indices[argname]
        yield ParamArgKey(argname, param_index, scoped_item_path, item_cls)

