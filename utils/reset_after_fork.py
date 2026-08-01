
def reset_after_fork():
    global lock
    loop[0] = None
    iothread[0] = None
    lock = None

