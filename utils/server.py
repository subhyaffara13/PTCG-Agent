
def server(msg: str, q: Queue[str]) -> None:
    server = IPCServer(CONNECTION_NAME)
    q.put(server.connection_name)
    data = ""
    while not data:
        with server:
            server.write(msg)
            data = server.read()
    server.cleanup()

