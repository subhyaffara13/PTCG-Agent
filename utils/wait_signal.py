
def wait_signal(hdl: _SymmetricMemory, peer: int) -> None:
    r"""
    wait_signal(hdl, peer) -> None

    Wait for a signal from a peer.

    Args:
        hdl (SymmetricMemory): the symmetric memory handle on which to wait for a signal.
        peer (int): the peer to wait for a signal from.
    """
    backend = get_backend(hdl.device)
    # See note in `put_signal` about `_SymmetricMemory` vs TorchBind type.
    hdl_boxed = hdl.boxed() if hasattr(hdl, "boxed") else hdl
    if backend == "NCCL":
        torch.ops.symm_mem.nccl_wait_signal(hdl_boxed, peer)
    # TODO: other backends' dispatch goes here
    else:
        raise ValueError(f"wait_signal: unsupported backend: {backend}")

