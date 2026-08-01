
def triton_config_to_hashable(cfg: Config) -> Hashable:
    """
    Convert triton config to a tuple that can uniquely identify it. We can use
    the return value as a dictionary key.
    """
    # pyrefly: ignore [missing-attribute]
    items = sorted(cfg.kwargs.items())
    # pyrefly: ignore [missing-attribute]
    items.append(("num_warps", cfg.num_warps))
    # pyrefly: ignore [missing-attribute]
    items.append(("num_stages", cfg.num_stages))
    return tuple(items)

