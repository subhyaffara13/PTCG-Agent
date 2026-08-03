import sys

def disable_cache_limit() -> Generator[None, None, None]:
    prior = config.recompile_limit
    # pyrefly: ignore [bad-assignment]
    config.recompile_limit = sys.maxsize
    prior_acc_limit = config.accumulated_recompile_limit
    # pyrefly: ignore [bad-assignment]
    config.accumulated_recompile_limit = sys.maxsize

    try:
        yield
    finally:
        config.recompile_limit = prior
        config.accumulated_recompile_limit = prior_acc_limit

