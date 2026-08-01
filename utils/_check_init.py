
def _check_init():
    if not _module_init():
        raise RuntimeError("pygame.midi not initialised.")

