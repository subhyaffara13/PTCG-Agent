
def align_runtime_estimations_across_all_distributed_ranks(
    snodes: list[BaseSchedulerNode],
):
    from torch._inductor.scheduler import _get_mm_like_fn

    runtime_estimations = {}
    runtime_estimations_for_mms = {}

    for snode in snodes:
        runtime_estimations[snode] = snode.get_estimated_runtime()
        if _get_mm_like_fn(snode) is not None:
            runtime_estimations_for_mms[snode] = runtime_estimations[snode]

    import torch.distributed as dist
    from torch.distributed.distributed_c10d import _get_default_group

    world_size = dist.get_world_size()
    pg = _get_default_group()
    gathered_runtime_estimations_for_mms: list[list[float]] = [
        [] for _ in range(world_size)
    ]
    dist.all_gather_object(
        gathered_runtime_estimations_for_mms,
        list(runtime_estimations_for_mms.values()),
        pg,
    )
    median_runtime_estimations_for_mms = torch.median(
        torch.tensor(gathered_runtime_estimations_for_mms), dim=0
    ).values.tolist()
    for idx, snode in enumerate(runtime_estimations_for_mms.keys()):
        runtime_estimations_for_mms[snode] = median_runtime_estimations_for_mms[idx]

    for snode in snodes:
        if snode in runtime_estimations_for_mms:
            runtime_estimations[snode] = runtime_estimations_for_mms[snode]
        snode.override_estimated_runtime = runtime_estimations[snode]

