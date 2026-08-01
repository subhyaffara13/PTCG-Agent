
def _make_config_key_from_heuristics_kernel(kernel) -> ConfigKey:
    """Build config key from nvMatmulHeuristics kernel config struct."""
    return (
        kernel.cta[0],
        kernel.cta[1],
        kernel.cluster[0],
        kernel.cluster[1],
    )

