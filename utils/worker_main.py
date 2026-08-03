import os

def worker_main() -> Generator[None, None, None]:
    """
    This is a context manager that wraps your main entry function. This combines
    the existing ``errors.record`` logic as well as a new ``_WorkerServer`` that
    exposes handlers via a unix socket specified by
    ``Torch_WORKER_SERVER_SOCKET``.

    Example

    ::

     @worker_main()
     def main():
         pass


     if __name__ == "__main__":
         main()

    """
    with ExitStack() as stack:
        socket_path = os.environ.get(TORCH_WORKER_SERVER_SOCKET)
        if socket_path is not None:
            stack.enter_context(_worker_server(socket_path))

        yield

