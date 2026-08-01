
def initialize_pg(init_method, rank: int, world_size: int) -> None:
    # This is for tests using `dist.barrier`.
    if not dist.is_initialized():
        dist.init_process_group(
            backend="gloo",
            init_method=init_method,
            rank=rank,
            world_size=world_size,
        )

