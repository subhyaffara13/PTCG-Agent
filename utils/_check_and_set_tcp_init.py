
def _check_and_set_tcp_init():
    # if we are running with TCP init, set main address and port
    # before spawning subprocesses, since different processes could find
    # different ports.
    use_tcp_init = os.environ.get("RPC_INIT_WITH_TCP", None)
    if use_tcp_init == "1":
        os.environ["MASTER_ADDR"] = "127.0.0.1"
        os.environ["MASTER_PORT"] = str(find_free_port())

