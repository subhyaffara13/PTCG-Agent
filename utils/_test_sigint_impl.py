
def _test_sigint_impl(backend, target_name, kwargs):
    import sys
    import matplotlib.pyplot as plt
    import os
    import threading

    plt.switch_backend(backend)

    def interrupter():
        if sys.platform == 'win32':
            from ctypes import windll, wintypes
            GenerateConsoleCtrlEvent = windll.kernel32.GenerateConsoleCtrlEvent
            GenerateConsoleCtrlEvent.argtypes = [wintypes.DWORD, wintypes.DWORD]
            GenerateConsoleCtrlEvent.restype = wintypes.BOOL
            GenerateConsoleCtrlEvent(0, 0)
        else:
            import signal
            os.kill(os.getpid(), signal.SIGINT)

    target = getattr(plt, target_name)
    timer = threading.Timer(1, interrupter)
    fig = plt.figure()
    fig.canvas.mpl_connect(
        'draw_event',
        lambda *args: print('DRAW', flush=True)
    )
    fig.canvas.mpl_connect(
        'draw_event',
        lambda *args: timer.start()
    )
    try:
        target(**kwargs)
    except KeyboardInterrupt:
        print('SUCCESS', flush=True)

