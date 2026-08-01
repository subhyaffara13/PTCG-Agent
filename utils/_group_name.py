
def _group_name(snode, with_bufs=False) -> str:
    ret = ""
    for n in snode.snodes:
        if ret:
            ret += "_"
        ret += n.get_name()
        if with_bufs:
            ret += f"{list(snode.get_buffer_names())}"
    return ret

