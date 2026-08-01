
def nccl_skip_if_lt_x_gpu(backend, x):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if backend != "nccl":
                return func(*args, **kwargs)
            if torch.cuda.is_available() and torch.cuda.device_count() >= x:
                return func(*args, **kwargs)
            test_skip = TEST_SKIPS[f"multi-gpu-{x}"]
            if not _maybe_handle_skip_if_lt_x_gpu(args, test_skip.message):
                sys.exit(test_skip.exit_code)

        return wrapper

    return decorator

