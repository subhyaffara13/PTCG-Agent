
def unoptimized_b2b_gemm(
    is_left_assoc: bool,
    subgraph: Subgraph,
    A: torch.Tensor,
    B: torch.Tensor,
    C: torch.Tensor,
    *,
    out: torch.Tensor,
) -> torch.Tensor:
    """
    The unoptimized version is used as a fallback when the b2b_gemm kernel is not beneficial.
    """
    if is_left_assoc:
        torch.mm(subgraph.graph_module(torch.mm(A, B)), C, out=out)
    else:
        torch.mm(A, subgraph.graph_module(torch.mm(B, C)), out=out)
    return out

