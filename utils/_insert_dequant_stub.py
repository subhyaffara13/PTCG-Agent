
def _insert_dequant_stub(
    node: Node,
    model: torch.nn.Module,
    named_modules: dict[str, torch.nn.Module],
    graph: Graph,
) -> Node:
    """
    Attach a `DeQuantStub` to the model and create a node that calls this
    `DeQuantStub` on the output of `node`, similar to how observers are inserted.
    """
    prefix = "dequant_stub_"
    get_new_dequant_stub_name = get_new_attr_name_with_prefix(prefix)
    dequant_stub_name = get_new_dequant_stub_name(model)
    dequant_stub = DeQuantStub()
    setattr(model, dequant_stub_name, dequant_stub)
    named_modules[dequant_stub_name] = dequant_stub
    with graph.inserting_after(node):
        return graph.call_module(dequant_stub_name, (node,))

