
def _update_group_membership(worker_info, my_devices, reverse_device_map, is_join):
    from . import api, TensorPipeAgent

    agent = cast(TensorPipeAgent, api._get_current_rpc_agent())
    ret = agent._update_group_membership(
        worker_info, my_devices, reverse_device_map, is_join
    )
    return ret

