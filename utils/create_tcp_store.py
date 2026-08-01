
def create_tcp_store(
    addr="localhost",
    world_size=1,
    is_master=True,
    timeout=timedelta(minutes=5),
    wait_for_workers=True,
    jit_class=False,
    use_libuv=True,
):
    """
    Creates a TCP store. Retries if the chosen port is already in use.
    """
    port = find_free_port()
    if jit_class:
        timeout_millisecond = int(timeout / timedelta(milliseconds=1))
        return torch.classes.dist_c10d.TCPStore(
            addr, port, world_size, is_master, timeout_millisecond
        )
    else:
        return c10d.TCPStore(
            addr,
            port,
            world_size,
            is_master,
            wait_for_workers=wait_for_workers,
            use_libuv=use_libuv,
        )

