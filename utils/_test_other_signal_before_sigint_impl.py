
def _test_other_signal_before_sigint_impl(backend, target_name, kwargs):
    import signal
    import matplotlib.pyplot as plt

    plt.switch_backend(backend)

    target = getattr(plt, target_name)

    fig = plt.figure()
    fig.canvas.mpl_connect('draw_event', lambda *args: print('DRAW', flush=True))

    timer = fig.canvas.new_timer(interval=1)
    timer.single_shot = True
    timer.add_callback(print, 'SIGUSR1', flush=True)

    def custom_signal_handler(signum, frame):
        timer.start()
    signal.signal(signal.SIGUSR1, custom_signal_handler)

    try:
        target(**kwargs)
    except KeyboardInterrupt:
        print('SUCCESS', flush=True)

