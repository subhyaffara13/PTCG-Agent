
def get_exhaustive_groupgemm_configs() -> list[CuTeGemmConfig]:
    """
    Returns the exhaustive configuration set for the Blackwell CuTeDSL Grouped GEMM kernel.
    For information regarding valid config sets, see:
    https://github.com/NVIDIA/cutlass/blob/main/examples/python/CuTeDSL/blackwell/grouped_gemm.py
    """

    # Tile_n is always the same regardless of 2cta
    tile_n_vals = [32, 64, 96, 128, 160, 192, 224, 256]

    # Valid clusters
    clusters_no_2cta = [
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 8),
        (1, 16),
        (2, 1),
        (2, 2),
        (2, 4),
        (2, 8),
        (4, 1),
        (4, 2),
        (4, 4),
        (8, 1),
        (8, 2),
        (16, 1),
    ]
    clusters_2cta = [
        (2, 1),
        (2, 2),
        (2, 4),
        (2, 8),
        (4, 1),
        (4, 2),
        (4, 4),
        (8, 1),
        (8, 2),
        (16, 1),
    ]

    configs: list[CuTeGemmConfig] = []

    for use_2cta, cluster_set, tile_m_range in [
        (False, clusters_no_2cta, [64, 128]),
        (True, clusters_2cta, [128, 256]),
    ]:
        for tensormap_update_mode, tile_m, tile_n, (cluster_m, cluster_n) in product(
            [TensorMapUpdateMode.SMEM, TensorMapUpdateMode.GMEM],
            tile_m_range,
            tile_n_vals,
            cluster_set,
        ):
            configs.append(
                CuTeGemmConfig(
                    tile_m,
                    tile_n,
                    cluster_m,
                    cluster_n,
                    USE_2_CTA=use_2cta,
                    TENSORMAP_UPDATE_MODE=tensormap_update_mode,
                )
            )

    return configs

