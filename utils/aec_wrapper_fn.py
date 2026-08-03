from typing import Callable

def aec_wrapper_fn(par_env_fn: Callable) -> Callable:
    """Converts class(pettingzoo.utils.env.ParallelEnv) -> class(pettingzoo.utils.env.AECEnv).

    Args:
        par_env_fn: The class to be wrapped.

    Example:
        class my_par_class(pettingzoo.utils.env.ParallelEnv):
            ...

        my_aec_class = aec_wrapper_fn(my_par_class)

    Note: applies the `OrderEnforcingWrapper` wrapper
    """

    def aec_fn(**kwargs):
        par_env = par_env_fn(**kwargs)
        aec_env = parallel_to_aec(par_env)
        return aec_env

    return aec_fn

