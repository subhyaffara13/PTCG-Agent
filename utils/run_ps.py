
def run_ps(trainers):
    timed_log("Start training")
    start = perf_counter()
    ps_rref = rpc.RRef(BatchUpdateParameterServer(len(trainers)))
    futs = [
        rpc.rpc_async(trainer, run_trainer, args=(ps_rref,)) for trainer in trainers
    ]

    torch.futures.wait_all(futs)
    stop = perf_counter()
    timed_log("Finish training")
    timed_log(f"Time spent training: {stop - start}s")

