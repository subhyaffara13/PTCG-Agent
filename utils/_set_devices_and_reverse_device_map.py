
def _set_devices_and_reverse_device_map(agent):
    from . import TensorPipeAgent

    agent = cast(TensorPipeAgent, agent)
    # Group state is retrieved from local agent
    # On initialization, tensorpipe agent retrieves information from all existing workers, so group state is valid
    my_worker_info = agent.get_worker_info()
    my_name = my_worker_info.name
    all_worker_infos = agent.get_worker_infos()
    # One round to get device_maps of all workers and construct reverse device maps
    all_device_counts, all_device_maps, all_devices, all_names = {}, {}, {}, []
    for worker_info in all_worker_infos:
        worker_name = worker_info.name
        if worker_name != my_name:
            # TODO: make async?
            device_count, device_map, devices = api.rpc_sync(
                worker_name, _get_device_infos
            )
        else:
            opts = agent._get_backend_options()
            device_count, device_map, devices = (
                torch.cuda.device_count(),
                opts.device_maps,
                opts.devices,
            )
        all_device_counts[worker_name] = device_count
        all_device_maps[worker_name] = device_map
        all_devices[worker_name] = devices
        all_names.append(worker_name)

    _validate_device_maps(
        all_names,
        all_device_counts,
        all_device_maps,
        all_devices,
        is_static_group=False,
    )
    reverse_device_maps = _create_reverse_mapping(my_name, all_names, all_device_maps)

    # Perform RPC call to all workers, including itself, to include newly joined worker information and device maps
    for worker_name in all_names:
        # Set device list for each worker
        all_devices[worker_name] = _create_device_list(
            all_devices[worker_name], all_device_maps[worker_name], reverse_device_maps
        )
        api.rpc_sync(
            worker_name,
            _update_group_membership,
            args=(my_worker_info, all_devices[worker_name], reverse_device_maps, True),
        )

