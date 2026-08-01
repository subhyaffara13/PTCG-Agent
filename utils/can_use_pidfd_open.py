
def can_use_pidfd_open():
    # Availability: Linux >= 5.3, Python >= 3.9
    if not hasattr(os, "pidfd_open"):
        return False
    try:
        pidfd = os.pidfd_open(os.getpid(), 0)
    except OSError as err:
        if err.errno in {errno.EMFILE, errno.ENFILE}:  # noqa: SIM103
            # transitory 'too many open files'
            return True
        # likely blocked by security policy like SECCOMP (EPERM,
        # EACCES, ENOSYS)
        return False
    else:
        os.close(pidfd)
        return True

