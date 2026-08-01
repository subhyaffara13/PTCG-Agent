
def get_size():
    comm = _get_comm()
    return comm.Get_size() if comm is not None else 1

