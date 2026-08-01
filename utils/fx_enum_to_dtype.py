
def fx_enum_to_dtype(gm: torch.fx.GraphModule, val: int) -> torch.fx.Node:
    return gm.graph.call_function(int_to_valid_dtype, (val,))

