
def _tensorpipe_init_backend_handler(
    store, name, rank, world_size, rpc_backend_options
):
    from . import TensorPipeAgent, TensorPipeRpcBackendOptions

    if not isinstance(store, dist.Store):
        raise TypeError(f"`store` must be a c10d::Store. {store}")

    if not isinstance(rpc_backend_options, TensorPipeRpcBackendOptions):
        raise TypeError(
            f"`rpc_backend_options` must be a `TensorPipeRpcBackendOptions`. {rpc_backend_options}"
        )

    device_count = torch.cuda.device_count()

    is_static_group = bool(world_size)
    # world_size is specified so this is a static group (ranks cannot join and leave)
    if is_static_group:
        # The agent's join method is required to behave like a barrier and perform
        # collective operations, for which it relies on a process group, instead of
        # re-implementing this on top of RPCs.
        group = _init_process_group(store, rank, world_size)

        reverse_device_maps, devices = _tensorpipe_exchange_and_check_all_device_maps(
            name,
            device_count,
            rpc_backend_options.device_maps,
            rpc_backend_options.devices,
            group,
        )

        if torch.cuda.is_available() and devices:
            # It's necessary to initialize PyTorch CUDA states here (e.g.,
            # CUDACachingAllocator). If this is missing, we could hit errors like
            # "allocator not initialized", because other processes might send
            # CUDA-related RPC request to this process before user code in this
            # process initializes its PyTorch CUDA states.
            torch.cuda.init()

        # TODO: add try-except and destroy _agent in all processes if any fails.
        agent = TensorPipeAgent(
            store,
            name,
            rank,
            world_size,
            rpc_backend_options,
            reverse_device_maps,
            devices,
        )

        api._init_rpc_states(agent)

        # Run one dummy round of RPC to initialize channels/transports. Without
        # this, it's easy to hit timeout in rpc.shutdown() if there is no other RPC
        # on that process before rpc.shutdown(), as the agent initialization can
        # take longer than 5s.
        api._all_gather(None, timeout=rpc_backend_options.rpc_timeout)
        # Need a barrier here to make sure no peers leave before the rank0 finishes
        # _all_gather
        group.barrier().wait()

        return agent
    # initialization for dynamic rpc (ranks can join and leave)
    else:
        with _group_membership_management(store, name, True):
            # Construct TPAgent with empty reverse_device_map and devices
            # these properties will be updated after initialization
            agent = TensorPipeAgent(
                store,
                name,
                rank,
                world_size,
                rpc_backend_options,
                {},
                [],
            )
            api._init_rpc_states(agent)

            try:
                # Notify all workers in group this rank has joined and set devices and reverse_device_map
                # This is a synchronous operation that completes once all existing ranks are updated
                _set_devices_and_reverse_device_map(agent)
            except Exception:
                api.shutdown()
                raise
            return agent

