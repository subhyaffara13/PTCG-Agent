
def _pre_init_placeholder():
    if not _is_init:
        raise error("pygame.camera is not initialized")

    # camera was init, and yet functions are not monkey patched. This should
    # not happen
    raise NotImplementedError()

