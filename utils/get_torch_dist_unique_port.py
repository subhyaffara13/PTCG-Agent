
def get_torch_dist_unique_port():
    """
    Returns a free port number that can be fed to `torch.distributed.launch`'s `--master_port` argument.

    Binds to port 0 to let the OS assign an available port, avoiding collisions from hardcoded ports
    and TCP TIME_WAIT issues between sequential subprocess launches.
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

