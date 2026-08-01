
def _check_and_unset_tcp_init():
    use_tcp_init = os.environ.get("RPC_INIT_WITH_TCP", None)
    if use_tcp_init == "1":
        del os.environ["MASTER_ADDR"]
        del os.environ["MASTER_PORT"]

