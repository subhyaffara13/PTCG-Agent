
def _ft_init_check():
    """
    Raises error if module is not init
    """
    if not _ft_init:
        raise error("fastevent system not initialized")

