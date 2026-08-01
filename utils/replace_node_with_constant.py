
def replace_node_with_constant(
    gm: torch.fx.GraphModule,
    node: torch.fx.Node,
    constant: torch.Tensor | None = None,
    name: str | None = None,
) -> None:
    g = gm.graph

    if name:
        qualname = name
    else:
        if not hasattr(gm, "_frozen_param_count"):
            gm._frozen_param_count = 0  # type: ignore[assignment]
        i = gm._frozen_param_count
        # pyrefly: ignore [bad-assignment]
        while True:
            qualname = f"_frozen_param{i}"
            if not hasattr(gm, qualname):
                break
            i += 1  # type: ignore[assignment, operator]

        gm._frozen_param_count = i + 1  # type: ignore[assignment, operator]

    with g.inserting_before(node):
        if constant is not None:
            new_input_node = g.create_node("get_attr", qualname, (), {})
        else:
            # this is the case for lifted constants
            new_input_node = g.create_node("placeholder", qualname, (), {})
        node.replace_all_uses_with(new_input_node)
        new_input_node.meta.update(node.meta)
        g.erase_node(node)
        new_input_node.name = node.name

    if constant is not None:
        # needed to suppress `does not reference an nn.Module, nn.Parameter, or buffer` warning
        gm.register_buffer(qualname, constant)
        setattr(gm, qualname, constant)
        # mark any constants created during freezing
        maybe_set_is_frozen_param(constant)


def replace_node_with_constant(gm, node, constant, name=None):
    g = gm.graph

    if name:
        qualname = name
    else:
        if not hasattr(gm, "_frozen_param_count"):
            gm._frozen_param_count = 0
        i = gm._frozen_param_count

        while True:
            qualname = f"_frozen_param{i}"
            if not hasattr(gm, qualname):
                break
            i += 1

        gm._frozen_param_count = i + 1

    with g.inserting_before(node):
        new_input_node = g.create_node("get_attr", qualname, (), {})
        node.replace_all_uses_with(new_input_node)
        new_input_node.meta.update(node.meta)
        g.erase_node(node)

    # needed to suppress `does not reference an nn.Module, nn.Parameter, or buffer` warning
    gm.register_buffer(qualname, constant)
    setattr(gm, qualname, constant)

