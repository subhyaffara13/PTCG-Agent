
def _reorder_submodules(
    parent: torch.nn.Module, fqn_order: dict[str, int], prefix: str = ""
):
    # TODO Can be optimized by adding submodules ahead of time.
    if prefix == "":
        for fqn in list(fqn_order.keys())[1:]:
            if _get_submodule(parent, fqn) is None:
                _add_submodule(parent, fqn, torch.nn.Module())

    children = []
    for name, child in list(parent._modules.items()):
        if child is None:
            continue
        fqn = prefix + name
        _reorder_submodules(child, fqn_order, prefix=fqn.split("@")[0] + ".")
        delattr(parent, name)
        base_fqn = fqn.split("@")[0]
        children.append(
            (fqn_order.get(fqn, fqn_order.get(base_fqn, len(fqn_order))), name, child)
        )
    children.sort(key=operator.itemgetter(0))
    for _, name, child in children:
        parent.register_module(name, child)

