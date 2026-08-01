
def _sharding_worker_init_fn(worker_init_fn, world_size, rank_id, worker_id) -> None:
    global_worker_id = worker_id
    info = torch.utils.data.get_worker_info()
    if info is None:
        raise AssertionError("Worker info is None in sharding worker init function")
    total_workers = info.num_workers
    datapipe = info.dataset
    if not isinstance(datapipe, (IterDataPipe, MapDataPipe)):
        raise AssertionError(
            "datapipe must be an instance of IterDataPipe or MapDataPipe"
        )
    # To distribute elements across distributed process evenly, we should shard data on distributed
    # processes first then shard on worker processes
    total_workers *= world_size
    global_worker_id = global_worker_id * world_size + rank_id
    # For BC, use default SHARDING_PRIORITIES
    torch.utils.data.graph_settings.apply_sharding(
        datapipe, total_workers, global_worker_id
    )
    if worker_init_fn is not None:
        worker_init_fn(worker_id)

