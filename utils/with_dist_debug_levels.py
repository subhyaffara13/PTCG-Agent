import os

def with_dist_debug_levels(levels):
    """
    Runs a test for each distributed debug level specified in levels.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_level = os.environ.get("TORCH_DISTRIBUTED_DEBUG", None)
            for level in levels:
                os.environ["TORCH_DISTRIBUTED_DEBUG"] = level
                c10d.set_debug_level_from_env()
                ret = func(*args, **kwargs)
                c10d.barrier()
                if old_level is not None:
                    os.environ["TORCH_DISTRIBUTED_DEBUG"] = old_level
            # Only returns test return for last test, but since these are
            # unittests the return value is not really used and earlier tests
            # would've raised had they failed.
            return ret

        return wrapper

    return decorator

