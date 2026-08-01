
def optimize_socket(sock: socket.socket) -> None:
  try:
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVBUF, constants.SOCKET_BUFFER_SIZE
    )
    sock.setsockopt(
        socket.SOL_SOCKET, socket.SO_SNDBUF, constants.SOCKET_BUFFER_SIZE
    )
  except OSError as e:
    logging.error('Failed to optimize socket: %s', e)

