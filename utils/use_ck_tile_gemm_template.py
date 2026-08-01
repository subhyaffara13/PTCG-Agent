
def use_ck_tile_gemm_template(layout: Layout, m: int, n: int, k: int) -> bool:
    from .virtualized import V

    return (
        _use_autotune_backend("CKTILE")
        and use_ck_template(layout)
        and V.graph.sizevars.optimization_hint(m * n * k, fallback=-1) > 0
    )

