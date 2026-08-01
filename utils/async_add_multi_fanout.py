
def async_add_multi_fanout(to, x, num, step):
    futs = []
    for i in range(num):
        if i == 0:
            futs.append(rpc.rpc_async(to, torch.add, args=(x, step)))
        else:
            futs.append(rpc.rpc_async(to, torch.add, args=(0, step)))

    # TODO: use torch.futures.collect_all
    lock = Lock()
    state = {"cnt": 0, "ret": torch.zeros_like(x)}
    ret_future = torch.futures.Future()

    def inc_and_set(fut):
        with lock:
            state["cnt"] += 1
            state["ret"] += fut.wait()
            if state["cnt"] >= len(futs):
                ret_future.set_result(state["ret"])

    for fut in futs:
        fut.then(inc_and_set)

    return ret_future

