
def _uninstall_threaded_pg():
    global _ctx_manager
    dist.distributed_c10d._world = _old_pg_world
    # Restore autograd multithreading state that was disabled in _install_threaded_pg
    if _ctx_manager is not None:
        _ctx_manager.__exit__(None, None, None)
        _ctx_manager = None

