
def _share_memory_lock_protected(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        to_free = None
        to_wait = None
        with _share_memory_lock:
            key = self._cdata
            if key in _share_memory_map:
                to_wait = _share_memory_map[key]
            else:
                _share_memory_map[key] = threading.RLock()
                _share_memory_map[key].acquire()
                to_free = key

        # If we're already in the process of sharing the storage, wait
        # for it to be done.
        if to_wait is not None:
            with to_wait:
                pass

        try:
            return fn(self, *args, **kwargs)
        finally:
            # If we acquired the storage lock here and we're done working on it
            # we can now release it and free the entry.
            if to_free is not None:
                # Ensure that the cdata from the storage didn't change and only
                # the data_ptr did.
                if self._cdata != to_free:
                    raise AssertionError(
                        f"storage cdata changed unexpectedly: expected {to_free}, got {self._cdata}"
                    )
                with _share_memory_lock:
                    _share_memory_map[to_free].release()
                    del _share_memory_map[to_free]

    return wrapper

