
def hop_schema_from_fx_node(node):
    from torchgen.gen_schema_utils import FunctionSchemaGen

    hop = node.target
    if not isinstance(hop, torch._ops.HigherOrderOperator):
        raise RuntimeError("fx_node's target must be a hop.")

    def _collect_example_val(node):
        meta_val = node.meta.get("val", None)
        if meta_val is None:
            if node.op != "get_attr":
                raise AssertionError(
                    f"node.op must be 'get_attr' when val is None, got {node.op!r}"
                )
            meta_val = getattr(node.graph.owning_module, node.target)
        return meta_val

    example_inputs = []
    for arg in node.args:
        if isinstance(arg, (torch.fx.Node, torch.fx.node.Node)):
            example_inputs.append(_collect_example_val(arg))
        elif isinstance(
            arg, (torch.fx.immutable_collections.immutable_list, list, tuple)
        ):
            example_inputs.append([_collect_example_val(x) for x in arg])
        else:
            raise RuntimeError(f"Unsupported arg type {type(arg)}")

    # Bound the arguments to make sure number of inputs are correct
    bound_args: inspect.BoundArguments = inspect.signature(hop.__call__).bind(
        *example_inputs
    )

    # We treat example_output as a single value in return. This is to differentiate 1. return a single val
    # vs 2. return a tuple with one element.
    example_output = _collect_example_val(node)
    return FunctionSchemaGen.from_example(
        hop._name, tuple(bound_args.arguments.items()), (list(example_output),)
    )

