
def put_signal(src: torch.Tensor, hdl: _SymmetricMemory, peer: int) -> None:
    r"""
    put_signal(src, hdl, peer) -> None

    Put data to a peer's symmetric memory and signal the peer.

    Args:
        src (torch.Tensor): the source tensor to read data from.
        hdl (SymmetricMemory): the symmetric memory to put data to.
        peer (int): the peer to put data to.
    """
    backend = get_backend(src.device)
    # `hdl` is a pybind `_SymmetricMemory` object. Dispatcher expects the
    # TorchBind custom class type `__torch__.torch.classes.c10d.SymmetricMemory`.
    # Convert via `.boxed()`.
    hdl_boxed = hdl.boxed() if hasattr(hdl, "boxed") else hdl
    if backend == "NCCL":
        torch.ops.symm_mem.nccl_put_signal(src, hdl_boxed, peer)
    # TODO: other backends' dispatch goes here
    else:
        raise ValueError(f"put_signal: unsupported backend: {backend}")

