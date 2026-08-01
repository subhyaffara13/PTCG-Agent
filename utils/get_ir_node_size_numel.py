
def get_ir_node_size_numel(size: torch.Size, fallback: int = 4096 * 4096) -> int:
    numel = sympy_product(size)
    if isinstance(numel, sympy.Integer):
        return int(numel)
    return V.graph.sizevars.optimization_hint(numel, fallback=fallback)

