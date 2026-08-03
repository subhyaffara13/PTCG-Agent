import os

def require_exact_world_size(world_size):
    if int(os.environ["WORLD_SIZE"]) != world_size:
        return skip_but_pass_in_sandcastle(
            f"Test requires an exact world size of {world_size:d}"
        )
    return lambda func: func

