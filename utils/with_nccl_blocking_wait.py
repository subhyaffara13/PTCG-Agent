
def with_nccl_blocking_wait(func):
    """
    Convenience decorator to set/unset TORCH_NCCL_BLOCKING_WAIT flag. Note that use of
    this decorator will override the setting of TORCH_NCCL_ASYNC_ERROR_HANDLING for
    the particular test. After the test, both TORCH_NCCL_BLOCKING_WAIT and
    TORCH_NCCL_ASYNC_ERROR_HANDLING will be restored to their original values.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Save and unset TORCH_NCCL_ASYNC_ERROR_HANDLING
        try:
            cached_nccl_async_error_handling: str | None = os.environ[
                "TORCH_NCCL_ASYNC_ERROR_HANDLING"
            ]
            del os.environ["TORCH_NCCL_ASYNC_ERROR_HANDLING"]
        except KeyError:
            # TORCH_NCCL_ASYNC_ERROR_HANDLING was unset
            cached_nccl_async_error_handling = None

        # Save val of TORCH_NCCL_BLOCKING_WAIT and set it.
        try:
            cached_nccl_blocking_wait: str | None = os.environ[
                "TORCH_NCCL_BLOCKING_WAIT"
            ]
        except KeyError:
            cached_nccl_blocking_wait = None
        finally:
            os.environ["TORCH_NCCL_BLOCKING_WAIT"] = "1"

        try:
            ret = func(*args, **kwargs)
            return ret
        finally:
            # restore old values.
            if cached_nccl_async_error_handling is not None:
                os.environ["TORCH_NCCL_ASYNC_ERROR_HANDLING"] = (
                    cached_nccl_async_error_handling
                )

            if cached_nccl_blocking_wait is not None:
                os.environ["TORCH_NCCL_BLOCKING_WAIT"] = cached_nccl_blocking_wait

    return wrapper

