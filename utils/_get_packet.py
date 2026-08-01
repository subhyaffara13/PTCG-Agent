
def _get_packet(qualname, op_module):
    op, overload_names = torch._C._jit_get_operation(qualname)
    if op is not None:
        # let the script frontend know that op is identical to the builtin op
        # with qualified_op_name
        torch.jit._builtins._register_builtin(op, qualname)
        op.__module__ = op_module
    return op, overload_names

