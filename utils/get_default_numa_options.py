
def get_default_numa_options():
    """
    When using elastic agent, if no numa options are provided, we will use these
    as the default.

    For external use cases, we return None, i.e. no numa binding. If you would like
    to use torch's automatic numa binding capabilities, you should provide
    NumaOptions to your launch config directly or use the numa binding option
    available in torchrun.

    Must return None or NumaOptions, but not specifying to avoid circular import.
    """
    return None

