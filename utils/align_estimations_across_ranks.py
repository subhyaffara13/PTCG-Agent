
def align_estimations_across_ranks(
    estimations: dict[fx.Node, float],
) -> dict[fx.Node, float]:
    """Align runtime estimations across distributed ranks using median.

    All ranks must make identical scheduling decisions, so we gather each
    rank's values and take the median. All nodes in estimations are aligned.

    Returns a new estimations dict with aligned values.
    """
    import torch.distributed as dist
    from torch._subclasses.fake_tensor import unset_fake_temporarily
    from torch.distributed.distributed_c10d import _get_default_group

    nodes = list(estimations.keys())
    if not nodes:
        return {}

    local_values = [estimations[n] for n in nodes]

    world_size = dist.get_world_size()
    pg = _get_default_group()

    with unset_fake_temporarily():
        gathered: list[list[float]] = [[] for _ in range(world_size)]
        dist.all_gather_object(gathered, local_values, pg)
        medians = torch.median(torch.tensor(gathered), dim=0).values.tolist()

    return dict(zip(nodes, medians))

