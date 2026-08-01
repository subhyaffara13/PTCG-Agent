
def _get_unique_devices_(module):
    return {p.device for p in module.parameters() if p.device.type != "meta"} | {
        p.device for p in module.buffers() if p.device.type != "meta"
    }

