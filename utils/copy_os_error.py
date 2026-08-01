
def copy_os_error(e: OSError) -> OSError:
    new = OSError(*e.args)
    new.errno = e.errno
    new.strerror = e.strerror
    new.filename = e.filename
    if e.filename2:
        new.filename2 = e.filename2
    return new

