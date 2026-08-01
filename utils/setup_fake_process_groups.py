
def setup_fake_process_groups(
    group_info: dict[str, dict[str, int]],
) -> None:
    """
    Set up fake process groups for repro execution.

    Args:
        group_info: dict mapping group_name -> {'size': group_size, 'rank': rank}
    """
    import torch.distributed as dist
    from torch.testing._internal.distributed.fake_pg import FakeStore

    if not group_info:
        return

    world_size = max(info["size"] for info in group_info.values())

    global_rank = 0
    for info in group_info.values():
        if info["size"] == world_size:
            global_rank = info["rank"]
            break

    store = FakeStore()
    dist.init_process_group(
        backend="fake",
        rank=global_rank,
        world_size=world_size,
        store=store,
    )

    default_pg = dist.distributed_c10d._get_default_group()
    torch._C._distributed_c10d._unregister_all_process_groups()

    for group_name, info in group_info.items():
        group_size = info["size"]
        if group_size == world_size:
            # pyrefly: ignore[bad-argument-type]
            torch._C._distributed_c10d._register_process_group(group_name, default_pg)
        else:
            ranks = list(range(group_size))
            new_pg = dist.new_group(ranks)
            # pyrefly: ignore[bad-argument-type]
            torch._C._distributed_c10d._register_process_group(group_name, new_pg)

