
def abort_xet_session():
    """Abort the global xet session after a KeyboardInterrupt.

    Cancels any in-flight Rust operation and clears the session so the next
    call to :func:`get_xet_session` starts fresh (notebook-friendly).
    """
    _GLOBAL_XET_HOLDER.sigint_abort()

