
def _get_comm():
    try:
        from mpi4py import MPI  # noqa: PLC0415

        comm = MPI.COMM_WORLD
        return comm
    except ImportError:
        return None

