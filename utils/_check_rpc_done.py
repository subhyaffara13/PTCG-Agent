
def _check_rpc_done(rank_distance):
    while not rpc_done[rank_distance]:
        time.sleep(0.1)

