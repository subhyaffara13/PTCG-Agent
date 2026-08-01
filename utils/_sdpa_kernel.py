
def _sdpa_kernel(backends: Iterable, set_priority: bool = False) -> None:
    for name, val in _backend_names.items():
        enabled = getattr(SDPBackend, val) in backends
        getattr(torch._C, f"_set_sdp_use_{name}")(enabled)
    if set_priority:
        # backends should be a unique list
        user_priority = [int(backend) for backend in backends]
        previous_priority = torch._C._get_sdp_priority_order()
        for backend in previous_priority:
            if backend not in user_priority:
                user_priority.append(int(backend))
        torch._C._set_sdp_priority_order(user_priority)

