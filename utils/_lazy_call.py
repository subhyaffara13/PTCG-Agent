
def _lazy_call(callable, **kwargs):
    with _initialization_lock:
        if is_initialized():
            callable()
        else:
            # TODO(torch_deploy): this accesses linecache, which attempts to read the
            # file system to get traceback info. Patch linecache or do something
            # else here if this ends up being important.
            global _lazy_seed_tracker
            if kwargs.get("seed_all", False):
                _lazy_seed_tracker.queue_seed_all(callable, traceback.format_stack())
            elif kwargs.get("seed", False):
                _lazy_seed_tracker.queue_seed(callable, traceback.format_stack())
            else:
                # Don't store the actual traceback to avoid memory cycle
                _queued_calls.append((callable, traceback.format_stack()))


def _lazy_call(callable, **kwargs):
    with _initialization_lock:
        if is_initialized():
            return callable()
        else:
            global _lazy_seed_tracker
            if kwargs.get("seed_all", False):
                _lazy_seed_tracker.queue_seed_all(callable, traceback.format_stack())
            elif kwargs.get("seed", False):
                _lazy_seed_tracker.queue_seed(callable, traceback.format_stack())
            else:
                _queued_calls.append((callable, traceback.format_stack()))


def _lazy_call(callable, **kwargs) -> None:
    if is_initialized():
        callable()
    else:
        global _lazy_seed_tracker
        if kwargs.get("seed_all", False):
            _lazy_seed_tracker.queue_seed_all(callable, traceback.format_stack())
        elif kwargs.get("seed", False):
            _lazy_seed_tracker.queue_seed(callable, traceback.format_stack())
        else:
            # Don't store the actual traceback to avoid memory cycle
            _queued_calls.append((callable, traceback.format_stack()))

