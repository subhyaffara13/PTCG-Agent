
def _pop_mode_temporarily():
    old = _pop_mode()
    try:
        yield old
    finally:
        _push_mode(old)


def _pop_mode_temporarily(k: DispatchKey | None = None):
    old = _pop_mode(k)
    try:
        yield old
    finally:
        _push_mode(old)

