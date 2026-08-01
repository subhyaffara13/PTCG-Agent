
def can_use_kqueue():
    # Availability: macOS, BSD
    names = (
        "kqueue",
        "KQ_EV_ADD",
        "KQ_EV_ONESHOT",
        "KQ_FILTER_PROC",
        "KQ_NOTE_EXIT",
    )
    if not all(hasattr(select, x) for x in names):
        return False
    kq = None
    try:
        kq = select.kqueue()
        kev = select.kevent(
            os.getpid(),
            filter=select.KQ_FILTER_PROC,
            flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
            fflags=select.KQ_NOTE_EXIT,
        )
        kq.control([kev], 1, 0)
        return True
    except OSError as err:
        if err.errno in {errno.EMFILE, errno.ENFILE}:  # noqa: SIM103
            # transitory 'too many open files'
            return True
        return False
    finally:
        if kq is not None:
            kq.close()

