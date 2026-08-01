
def _add_op(
    graph_context: GraphContext,
    opname: str,
    *args: torch.Tensor | _C.Value,
    outputs: int = 1,
    **kwargs,
):
    """Creates an ONNX operator "opname", taking "args" as inputs and attributes "kwargs".

    The set of operators and the inputs/attributes they take
    is documented at https://github.com/onnx/onnx/blob/master/docs/Operators.md

    Args:
        graph_context: The Torch Graph or Block.
        opname: The ONNX operator name, e.g., `Abs` or `Add`, or an operator qualified
            with a namespace, e.g., `aten::add`.
        args: The inputs to the operator; usually provided
            as arguments to the `symbolic` definition.
        outputs: The number of outputs this operator returns.
            By default an operator is assumed to return a single output.
            If `outputs` is greater than one, this functions returns a tuple
            of output `Value`, representing each output of the ONNX operator
            in order.
        kwargs: The attributes of the ONNX operator, whose keys are named
            according to the following convention: `alpha_f` indicates
            the `alpha` attribute with type `f`.  The valid type specifiers are
            `f` (float), `i` (int), `s` (string) or `t` (Tensor).  An attribute
            specified with type float accepts either a single float, or a
            list of floats (e.g., you would say `dims_i` for a `dims` attribute
            that takes a list of integers).

    Returns:
        (Union[_C.Value, Tuple[_C.Value, ...]])
        The value representing the single output of this operator (see the `outputs`
        keyword argument for multi-return nodes).
    """
    inputs = [_const_if_tensor(graph_context, arg) for arg in args]
    # Filter out None attributes, this can be convenient client side because
    # now they can pass through None attributes, and have them not show up
    attributes = {k: v for k, v in kwargs.items() if v is not None}

    if "::" not in opname:
        opname = "onnx::" + opname

    node = _create_node(
        graph_context.block,
        opname,
        inputs,
        attributes,
        params_dict=graph_context.params_dict,
        opset_version=graph_context.opset,
        n_outputs=outputs,
        shape_inference=GLOBALS.onnx_shape_inference,
    )
    graph_context.new_nodes.append(node)

    if outputs == 1:
        return node.output()
    return tuple(node.outputs())

