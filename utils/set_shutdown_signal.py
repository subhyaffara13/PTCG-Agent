
def set_shutdown_signal():
    global shutdown_signal
    with shutdown_signal:
        shutdown_signal.notify()

