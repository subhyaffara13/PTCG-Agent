
def quit():
    global _is_init, Camera, list_cameras
    # reset to their respective pre-init placeholders
    list_cameras = _pre_init_placeholder
    Camera = _PreInitPlaceholderCamera

    _is_init = False


def quit():  # pylint: disable=redefined-builtin
    """uninitialize the midi module
    pygame.midi.quit(): return None


    Called automatically atexit if you don't call it.

    It is safe to call this function more than once.
    """
    if _module_init():
        # TODO: find all Input and Output classes and close them first?
        _pypm.Terminate()
        _module_init(False)


def quit():
    global vidcap
    vidcap = None


def quit():
    """cleans up everything."""
    global _wq, _use_workers
    _wq.stop()
    _wq = None
    _use_workers = False

