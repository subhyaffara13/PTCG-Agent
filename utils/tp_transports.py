
def tp_transports():
    """
    If the machine has Libfabric EFA interfaces and EFA software components installed it may cause
    'RuntimeError: In operator() at tensorpipe/common/ibv.h:172 "": Operation not supported' if tensorpipe
    uses InfiniBand transport, so we exclude it from tensorpipe transports,
    see https://github.com/pytorch/pytorch/issues/73885 and https://github.com/pytorch/pytorch/issues/65022
    """
    return ["shm", "uv"] if has_efa() else None

