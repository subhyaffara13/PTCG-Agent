
def server_multi_message_echo(q: Queue[str]) -> None:
    server = IPCServer(CONNECTION_NAME)
    q.put(server.connection_name)
    data = ""
    with server:
        while data != "quit":
            data = server.read()
            server.write(data)
    server.cleanup()

