from typing import Callable

def parallel_wrapper_fn(env_fn: Callable) -> Callable:
    def par_fn(**kwargs):
        env = env_fn(**kwargs)
        env = aec_to_parallel_wrapper(env)
        return env

    return par_fn

