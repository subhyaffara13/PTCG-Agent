
def _cur_sdpa_kernel_backends(with_priority: bool = False):
    backends = []
    for name, val in _backend_names.items():
        if getattr(torch._C, f"_get_{name}_sdp_enabled")():
            backends.append(getattr(SDPBackend, val))
    if with_priority:
        curr_priority = torch._C._get_sdp_priority_order()
        backends = sorted(
            backends, key=lambda backend: curr_priority.index(int(backend))
        )
    return backends

