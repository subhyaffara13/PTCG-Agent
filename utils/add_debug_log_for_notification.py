
def add_debug_log_for_notification(
    connection: "MaintNotificationsAbstractConnection",
    notification: Union[str, MaintenanceNotification],
):
    if logger.isEnabledFor(logging.DEBUG):
        socket_address = None
        try:
            socket_address = (
                connection._sock.getsockname() if connection._sock else None
            )
            socket_address = socket_address[1] if socket_address else None
        except (AttributeError, OSError):
            pass

        logger.debug(
            f"Handling maintenance notification: {notification}, "
            f"with connection: {connection}, connected to ip {connection.get_resolved_ip()}, "
            f"local socket port: {socket_address}",
        )

