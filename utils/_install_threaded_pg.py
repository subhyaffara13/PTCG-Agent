
def _install_threaded_pg():
    global _old_pg_world
    global _ctx_manager
    _old_pg_world = dist.distributed_c10d._world
    dist.distributed_c10d._world = ThreadLocalWorld()
    _ctx_manager = torch.autograd.set_multithreading_enabled(False)

    return dist.distributed_c10d._world

