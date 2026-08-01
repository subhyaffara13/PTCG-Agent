
def _init_rpc_states(agent):
    worker_infos = agent.get_worker_infos()
    global _ALL_WORKER_NAMES
    _ALL_WORKER_NAMES = {worker_info.name for worker_info in worker_infos}

    # NB: backend implementation might have already set the rpc_agent.
    if not _is_current_rpc_agent_set():
        _set_and_start_rpc_agent(agent)

