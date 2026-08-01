
def _log_spec_into_io_specs(
    spec: graph_signature.InputSpec,
    nodes: dict[str, torch.fx.Node],
    inputs_or_outputs: dict[str, torch._export.serde.schema.TensorMeta | str],
) -> dict[str, torch._export.serde.schema.TensorMeta | str]:
    # If dynamic is set to a constant input, it becomes a
    # symbolic argument, which is not a tensor.
    if isinstance(spec.arg, graph_signature.ConstantArgument):
        # Constant input does not have tensor_meta.
        return inputs_or_outputs
    # Symbolic arguments are not tensors, so it does not have tensor_meta,
    # but we need to provide a string representation for them to inform users.
    name = spec.arg.name
    if isinstance(
        spec.arg,
        (
            graph_signature.SymIntArgument,
            graph_signature.SymFloatArgument,
            graph_signature.SymBoolArgument,
        ),
    ):
        argument_to_str: dict[type[graph_signature.ArgumentSpec], str] = {
            graph_signature.SymIntArgument: "SymInt",
            graph_signature.SymFloatArgument: "SymFloat",
            graph_signature.SymBoolArgument: "SymBool",
        }
        inputs_or_outputs[name] = argument_to_str[type(spec.arg)]
        return inputs_or_outputs
    # FIXME: tensor_meta is None sometimes when the exported program still knows the shape/type
    inputs_or_outputs[name] = nodes[name].meta["tensor_meta"]
    return inputs_or_outputs

