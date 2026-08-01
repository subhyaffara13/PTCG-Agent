
def _check_op(op) -> None:
    """Check that the ``op`` is either isend or irecv."""
    if op not in [isend, irecv]:
        raise ValueError(
            "Invalid ``op``. Expected ``op`` "
            "to be of type ``torch.distributed.isend`` or "
            "``torch.distributed.irecv``."
        )

