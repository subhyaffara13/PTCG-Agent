
def get_device_states(*args) -> Tuple[List[int], List[torch.Tensor]]:
    # This will not error out if "arg" is a CPU tensor or a non-tensor type because
    # the conditionals short-circuit.
    fwd_device_ids = []

    def add_device_ids(arg):
        nonlocal fwd_device_ids
        if isinstance(arg, torch.Tensor) and arg.device.type not in {"cpu", "meta"}:
            fwd_device_ids.append(arg.get_device())
        return arg
    tree_map(add_device_ids, args)

    fwd_device_states = []
    device_module = _get_device_module(_infer_device_type(*args))
    for device_id in fwd_device_ids:
        with device_module.device(device_id):
            fwd_device_states.append(device_module.get_rng_state())

    return fwd_device_ids, fwd_device_states

