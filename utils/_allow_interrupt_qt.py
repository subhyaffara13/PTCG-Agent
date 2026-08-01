
def _allow_interrupt_qt(qapp_or_eventloop):
    """A context manager that allows terminating a plot by sending a SIGINT."""

    # Use QSocketNotifier to read the socketpair while the Qt event loop runs.

    def prepare_notifier(rsock):
        sn = QtCore.QSocketNotifier(rsock.fileno(), QtCore.QSocketNotifier.Type.Read)

        @sn.activated.connect
        def _may_clear_sock():
            # Running a Python function on socket activation gives the interpreter a
            # chance to handle the signal in Python land.  We also need to drain the
            # socket with recv() to re-arm it, because it will be written to as part of
            # the wakeup.  (We need this in case set_wakeup_fd catches a signal other
            # than SIGINT and we shall continue waiting.)
            try:
                rsock.recv(1)
            except BlockingIOError:
                # This may occasionally fire too soon or more than once on Windows, so
                # be forgiving about reading an empty socket.
                pass

        # We return the QSocketNotifier so that the caller holds a reference, and we
        # also explicitly clean it up in handle_sigint(). Without doing both, deletion
        # of the socket notifier can happen prematurely or not at all.
        return sn

    def handle_sigint(sn):
        sn.deleteLater()
        QtCore.QCoreApplication.sendPostedEvents(sn, QtCore.QEvent.Type.DeferredDelete)
        if hasattr(qapp_or_eventloop, 'closeAllWindows'):
            qapp_or_eventloop.closeAllWindows()
        qapp_or_eventloop.quit()

    return _allow_interrupt(prepare_notifier, handle_sigint)

