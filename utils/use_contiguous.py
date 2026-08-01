
def use_contiguous(m: _IntLike, n: _IntLike, k: _IntLike) -> bool:
    """
    Check if we should use the contiguous subgraph transform.
    This transform makes the second matrix contiguous before the matmul.
    """
    contiguous_threshold = config.rocm.contiguous_threshold

    # Similar conditions to decompose_k but for contiguous transform
    from torch._inductor.virtualized import V

    return (
        bool(torch.version.hip)  # Only relevant on AMD
        and V.graph.sizevars.statically_known_true(
            sympy.And(
                sympy.Ge(k, contiguous_threshold * m),
                sympy.Ge(k, contiguous_threshold * n),
            )
        )
        and not V.graph.aot_mode
        and not V.graph.cpp_wrapper
    )

