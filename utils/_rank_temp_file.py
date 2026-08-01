
def _rank_temp_file():
    if dist.get_rank() == 0:
        fd, name = tempfile.mkstemp()
        os.close(fd)
    else:
        name = None
    object_list = [name]
    dist.broadcast_object_list(object_list)
    name = object_list[0]
    try:
        yield name
    finally:
        if dist.get_rank() == 0:
            os.remove(name)

