
def get_max_tiles(default: int = 2) -> int:
    max_tiles = torch._inductor.config.triton.max_tiles
    return max_tiles if max_tiles is not None else default

