import os

def _join_cuda_home(*paths) -> str:
    """
    Join paths with CUDA_HOME, or raises an error if it CUDA_HOME is not set.

    This is basically a lazy way of raising an error for missing $CUDA_HOME
    only once we need to get any CUDA-specific path.
    """
    if CUDA_HOME is None:
        raise OSError('CUDA_HOME environment variable is not set. '
                      'Please set it to your CUDA install root.')
    return os.path.join(CUDA_HOME, *paths)

