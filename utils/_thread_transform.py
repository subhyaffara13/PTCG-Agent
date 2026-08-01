
def _thread_transform() -> nodes.Module:
    return parse(
        """
    class lock(object):
        def acquire(self, blocking=True, timeout=-1):
            return False
        def release(self):
            pass
        def __enter__(self):
            return True
        def __exit__(self, *args):
            pass
        def locked(self):
            return False

    def Lock(*args, **kwargs):
        return lock()
    """
    )

