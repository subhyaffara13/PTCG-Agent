
def _nccl_factory(
    store: Store,
    rank: int,
    world_size: int,
    timeout: timedelta,
    device: torch.device,
    **kwargs: object,
) -> ProcessGroup:
    from torch.distributed import ProcessGroupNCCL

    opts = ProcessGroupNCCL.Options()
    opts._timeout = timeout
    for k, v in kwargs.items():
        if not hasattr(opts, k):
            raise KeyError(f"Unknown option {k}")
        setattr(opts, k, v)

    backend_class = ProcessGroupNCCL(store, rank, world_size, opts)
    backend_class._set_sequence_number_for_group()
    backend_class.eager_connect_single_device(device)

    pg = ProcessGroup(store, rank, world_size)
    pg._set_default_backend(ProcessGroup.BackendType.NCCL)
    pg._register_backend(device, ProcessGroup.BackendType.NCCL, backend_class)

    return pg

