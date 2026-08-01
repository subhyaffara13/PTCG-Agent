
def find_first_sym_node(
    fwd_module_outputs: list[fx.Node] | tuple[fx.Node, ...],
) -> int:
    idx = len(fwd_module_outputs)
    for i in range(len(fwd_module_outputs) - 1, -1, -1):
        if not is_sym_node(fwd_module_outputs[i]):
            idx = i + 1
            break
    return idx

