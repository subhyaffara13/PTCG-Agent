
def get_out_arg_names(out_op: torch._ops.OpOverload) -> list[str]:
    """Get the names of out arguments for an out variant op."""
    schema = out_op._schema
    return [arg.name for arg in schema.arguments if _is_mutable_arg(arg)]

