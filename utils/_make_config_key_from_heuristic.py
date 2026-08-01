
def _make_config_key_from_heuristic(cfg: HeuristicConfig) -> ConfigKey:
    """Build config key from HeuristicConfig returned by nvMatmulHeuristics."""
    return (cfg.tile_m, cfg.tile_n, cfg.cluster_m, cfg.cluster_n)

