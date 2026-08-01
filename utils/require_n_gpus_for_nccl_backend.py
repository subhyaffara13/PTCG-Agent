
def require_n_gpus_for_nccl_backend(n, backend):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if backend == "nccl" and torch.cuda.device_count() < n:
                sys.exit(TEST_SKIPS[f"multi-gpu-{n}"].exit_code)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator

