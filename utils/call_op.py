
def call_op(op: OpOverload | HopInstance, args, kwargs):
    if isinstance(op, OpOverload):
        return op(*args, **kwargs)

    if not isinstance(op, HopInstance):
        raise AssertionError(f"Expected HopInstance, got {type(op)}")
    schema = op._schema
    bound_args = list(args)
    bound_kwargs = {}
    for arg in schema.arguments[len(bound_args) :]:
        if arg.name not in kwargs:
            raise AssertionError(f"arg {arg.name} not in kwargs: {kwargs}")
        val = kwargs[arg.name]
        if not arg.kwarg_only:
            bound_args.append(val)
        else:
            bound_kwargs[arg.name] = val

    if schema.tree_spec is not None:
        if len(bound_args) != len(schema.arguments) or len(bound_kwargs) != 0:
            raise AssertionError(
                f"Expected {len(schema.arguments)} bound_args and 0 bound_kwargs, "
                f"got {len(bound_args)} and {len(bound_kwargs)}"
            )
        args, kwargs = pytree.tree_unflatten(bound_args, schema.tree_spec)
        return op(*args, **kwargs)
    else:
        if len(bound_args) + len(bound_kwargs) != len(schema.arguments):
            raise AssertionError(
                f"Expected {len(schema.arguments)} total args, "
                f"got {len(bound_args)} + {len(bound_kwargs)}"
            )
        return op(*bound_args, **bound_kwargs)


def call_op(
    op_type: str,
    *args: ir.Value | None,
    _num_outputs: int = 1,
    _domain: str = "",
    **kwargs: int | float | str | bool | ir.Graph | ir.TensorProtocol | Sequence[int],
) -> Sequence[ir.Value]:
    """Call an operator with the given arguments and keyword arguments.

    Arguments are always inputs, while keyword arguments are attributes.
    """
    # This is a wrapper around the IR node creation that hooks into the _builder.OpRecorder
    # tracer so that all nodes created are recorded the same way as if we were to use
    # onnxscript ops directly.
    from onnxscript.ir import convenience as ir_convenience

    if _core.current_tracer is None:
        raise AssertionError("current_tracer must be non-None")
    tracer = _core.current_tracer

    inputs = list(args)

    # If final inputs are None, strip them from the node inputs
    for input in reversed(inputs):
        if input is not None:
            break
        inputs.pop()

    # Construct and filter out None attributes
    attributes = [
        attr
        for attr in ir_convenience.convert_attributes(kwargs)
        if attr.value is not None  # type: ignore[union-attr]
    ]
    tracer.nodes.append(
        node := ir.Node(
            _domain,
            op_type,
            inputs=inputs,
            attributes=attributes,
            num_outputs=_num_outputs,
            version=tracer.opset.version,
        )
    )
    return node.outputs

