
def _make_config_key_from_kernel_design(design) -> ConfigKey | None:
    """Build config key from cutlass_api kernel metadata.design."""
    if (
        hasattr(design, "tile_shape")
        and len(design.tile_shape) >= 2
        and hasattr(design, "cluster_shape")
        and len(design.cluster_shape) >= 2
    ):
        return (
            design.tile_shape[0],
            design.tile_shape[1],
            design.cluster_shape[0],
            design.cluster_shape[1],
        )
    return None

