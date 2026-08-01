
def ready_to_read(conns: Sequence[IPCBase], timeout: float | None = None) -> list[int]:
    """Wait until some connections are readable.

    Return index of each readable connection in the original list.
    """
    unread_messages = [i for i, conn in enumerate(conns) if conn.buffer]
    if unread_messages:
        # If we already have unread messages in the buffer, return those first.
        return unread_messages
    if sys.platform == "win32":
        # Windows doesn't support select() on named pipes. Instead, start an overlapped
        # ReadFile on each pipe (which internally creates an event via CreateEventW),
        # then WaitForMultipleObjects on those events for efficient OS-level waiting.
        # Any data consumed by the probe reads is stored into each connection's buffer
        # so the subsequent read_bytes() call will find it via frame_from_buffer().
        WAIT_FAILED = 0xFFFFFFFF
        pending: list[tuple[int, _winapi.Overlapped]] = []
        events: list[int] = []
        ready: list[int] = []

        for i, conn in enumerate(conns):
            try:
                ov, err = _winapi.ReadFile(conn.connection, 1, overlapped=True)
            except OSError:
                # Broken/closed pipe. Mimic Linux behavior here, caller will get
                # the exception when trying to read from this socket.
                ready.append(i)
                continue
            if err == _winapi.ERROR_IO_PENDING:
                events.append(ov.event)
                pending.append((i, ov))
            else:
                # Data was immediately available (err == 0 or ERROR_MORE_DATA)
                _, err = ov.GetOverlappedResult(True)
                data = ov.getbuffer()
                if data:
                    conn.buffer.extend(data)
                ready.append(i)

        # Wait only if nothing is immediately ready and there are pending operations
        if not ready and events:
            timeout_ms = int(timeout * 1000) if timeout is not None else _winapi.INFINITE
            res = _winapi.WaitForMultipleObjects(events, False, timeout_ms)
            if res == WAIT_FAILED:
                for _, ov in pending:
                    ov.cancel()
                raise IPCException(f"Failed to wait for connections: {_winapi.GetLastError()}")

        # Cancel all pending operations. CancelIoEx is asynchronous, so an
        # operation may have completed before the cancel took effect. We then
        # wait for all operations to finalize and check each result: completed
        # reads get their data saved and are marked ready; cancelled ones are
        # simply skipped. This avoids a race between checking if an operation
        # is signaled and cancelling it.
        for _, ov in pending:
            ov.cancel()
        for i, ov in pending:
            try:
                _, err = ov.GetOverlappedResult(True)
            except OSError as e:
                err = e.winerror
                # Cancellation is expected here; broken/disconnected pipes should be
                # surfaced as readable so the follow-up receive observes EOF/closure.
                if err not in (
                    _winapi.ERROR_OPERATION_ABORTED,
                    _winapi.ERROR_BROKEN_PIPE,
                    _winapi.ERROR_NETNAME_DELETED,
                ):
                    # Anything else is a real IPC failure, not part of the probe race.
                    raise
            if err == _winapi.ERROR_OPERATION_ABORTED:
                # Operation was successfully cancelled -- no data consumed.
                continue
            if err in (0, _winapi.ERROR_MORE_DATA):
                data = ov.getbuffer()
                if data:
                    conns[i].buffer.extend(data)
            ready.append(i)

        return ready

    else:
        connections = [conn.connection for conn in conns]
        ready, _, _ = select(connections, [], [], timeout)
        return [connections.index(r) for r in ready]

