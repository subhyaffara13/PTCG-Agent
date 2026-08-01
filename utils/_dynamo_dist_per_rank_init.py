
def _dynamo_dist_per_rank_init(
    rank, world_size, backend=None, init_pg=True, fake_pg=False
):
    # To avoid multiple inheritance from _dynamo.test_case.TestCase and MultiProcessTestCase,
    # Just manually implement the most important part of the dynamo behavior to reset/clear.
    if not fake_pg:
        torch.accelerator.set_device_index(rank)

    device_type = (
        acc.type if (acc := torch.accelerator.current_accelerator()) else "cpu"
    )
    if backend is None:
        backend = c10d.get_default_backend_for_device(device_type)

    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "6789"
    if init_pg:
        if fake_pg:
            store = torch.testing._internal.distributed.fake_pg.FakeStore()
            c10d.init_process_group(
                backend="fake",
                world_size=world_size,
                rank=rank,
                store=store,
            )
        else:
            c10d.init_process_group(backend=backend, rank=rank, world_size=world_size)
    torch._dynamo.reset()
    torch._dynamo.utils.counters.clear()
    try:
        yield
    finally:
        torch._dynamo.reset()
        torch._dynamo.utils.counters.clear()
        if init_pg:
            c10d.destroy_process_group()

