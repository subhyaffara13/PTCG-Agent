
def _export_operator_list(module: LiteScriptModule):
    r"""Return a set of root operator names (with overload name) that are used by any method in this mobile module."""
    return torch._C._export_operator_list(module._c)

