import functools

def profile_endpoint(sampling_rate: float = 1.0):
    """Decorator to sample endpoint hits and save to a profile file.

    Args:
        sampling_rate: Rate of requests to profile (0.0 to 1.0)
                      - 1.0: Profile all requests (100%)
                      - 0.1: Profile 1 in 10 requests (10%)
                      - 0.0: Profile no requests (0%)
    """

    def decorator(func):
        def set_last_profile_path(path: PathLib) -> None:
            global _last_profile_file_path
            _last_profile_file_path = path

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                is_sampling = _start_profiling_for_request(sampling_rate)
                file_path_obj = PathLib("endpoint_profile.pstat")
                set_last_profile_path(file_path_obj)
                try:
                    result = await func(*args, **kwargs)
                    if is_sampling:
                        _save_stats(file_path_obj)
                    return result
                except Exception:
                    if is_sampling:
                        _save_stats(file_path_obj)
                    raise

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                is_sampling = _start_profiling_for_request(sampling_rate)
                file_path_obj = PathLib("endpoint_profile.pstat")
                set_last_profile_path(file_path_obj)
                try:
                    result = func(*args, **kwargs)
                    if is_sampling:
                        _save_stats(file_path_obj)
                    return result
                except Exception:
                    if is_sampling:
                        _save_stats(file_path_obj)
                    raise

            return sync_wrapper

    return decorator

