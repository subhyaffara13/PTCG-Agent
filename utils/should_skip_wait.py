
def should_skip_wait(x: ir.IRNode) -> bool:
    return (id(V.graph), x.get_name()) in _bufs_to_skip_wait

