
def test_fig_sigint_override():
    from matplotlib.backends.backend_qt5 import _BackendQT5
    # Create a figure
    plt.figure()

    # Variable to access the handler from the inside of the event loop
    event_loop_handler = None

    # Callback to fire during event loop: save SIGINT handler, then exit
    def fire_signal_and_quit():
        # Save event loop signal
        nonlocal event_loop_handler
        event_loop_handler = signal.getsignal(signal.SIGINT)

        # Request event loop exit
        QtCore.QCoreApplication.exit()

    # Timer to exit event loop
    QtCore.QTimer.singleShot(0, fire_signal_and_quit)

    # Save original SIGINT handler
    original_handler = signal.getsignal(signal.SIGINT)

    # Use our own SIGINT handler to be 100% sure this is working
    def custom_handler(signum, frame):
        pass

    signal.signal(signal.SIGINT, custom_handler)

    try:
        # mainloop() sets SIGINT, starts Qt event loop (which triggers timer
        # and exits) and then mainloop() resets SIGINT
        matplotlib.backends.backend_qt._BackendQT.mainloop()

        # Assert: signal handler during loop execution is changed
        # (can't test equality with func)
        assert event_loop_handler != custom_handler

        # Assert: current signal handler is the same as the one we set before
        assert signal.getsignal(signal.SIGINT) == custom_handler

        # Repeat again to test that SIG_DFL and SIG_IGN will not be overridden
        for custom_handler in (signal.SIG_DFL, signal.SIG_IGN):
            QtCore.QTimer.singleShot(0, fire_signal_and_quit)
            signal.signal(signal.SIGINT, custom_handler)

            _BackendQT5.mainloop()

            assert event_loop_handler == custom_handler
            assert signal.getsignal(signal.SIGINT) == custom_handler

    finally:
        # Reset SIGINT handler to what it was before the test
        signal.signal(signal.SIGINT, original_handler)

