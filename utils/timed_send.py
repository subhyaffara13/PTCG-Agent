import time

def timed_send(manager: BuildManager, server: IPCServer, message: SccResponseMessage) -> None:
    t0 = time.time()
    send(server, message)
    manager.add_stats(scc_send_time=time.time() - t0)

