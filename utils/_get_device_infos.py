
def _get_device_infos():
    from . import TensorPipeAgent

    agent = cast(TensorPipeAgent, api._get_current_rpc_agent())
    opts = agent._get_backend_options()
    device_count = torch.cuda.device_count()
    if torch.cuda.is_available() and opts.devices:
        torch.cuda.init()
    return device_count, opts.device_maps, opts.devices

