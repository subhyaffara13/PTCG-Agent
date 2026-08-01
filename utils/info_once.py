
def info_once(self, *args, **kwargs):
    """
    This method is identical to `logger.info()`, but will emit the info with the same message only once

    Note: The cache is for the function arguments, so 2 different callers using the same arguments will hit the cache.
    The assumption here is that all warning messages are unique across the code. If they aren't then need to switch to
    another type of cache that includes the caller frame information in the hashing function.
    """
    self.info(*args, **kwargs)

