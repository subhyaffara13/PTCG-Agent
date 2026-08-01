
def _worker_server(socket_path: str) -> Generator[None, None, None]:
    from torch._C._distributed_c10d import _WorkerServer

    server = _WorkerServer(socket_path)
    try:
        yield
    finally:
        server.shutdown()

