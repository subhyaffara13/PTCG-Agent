
def use_decompose_k_choice(
    m: _IntLike, n: _IntLike, k: _IntLike, threshold_multiple: int = 1
) -> bool:
    from torch._inductor.virtualized import V

    decompose_k_threshold = config.triton.decompose_k_threshold * threshold_multiple

    return (
        V.graph.sizevars.statically_known_true(
            sympy.And(
                sympy.Ge(k, decompose_k_threshold * m),
                sympy.Ge(k, decompose_k_threshold * n),
            )
        )
        and not V.graph.aot_mode  # TODO: Support AOTI for decomposeK
        and not V.graph.cpp_wrapper
        and config.triton.num_decompose_k_splits > 0
    )

