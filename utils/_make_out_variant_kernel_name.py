
def _make_out_variant_kernel_name(out_op: torch._ops.OpOverload) -> str:
    """Build fully-qualified kernel name for an out-variant op."""
    ns = out_op.namespace
    op_name = out_op._schema.name.split("::")[1]
    overload = out_op._overloadname
    return f"torch.ops.{ns}.{op_name}.{overload}"

