
def make_matmul_triton_config(sizes: dict[str, int], num_warps: int, num_stages: int):
    config = {
        "XBLOCK": sizes.get("x"),
        "YBLOCK": sizes.get("y"),
        "ZBLOCK": sizes.get("z"),
        "R0_BLOCK": sizes.get("r"),
    }
    # Remove keys with None values (i.e., missing in sizes)
    config = {k: v for k, v in config.items() if v is not None}
    return Config(config, num_warps=num_warps, num_stages=num_stages)

