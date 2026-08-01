
def is_torch_neuroncore_available(check_device=True) -> bool:
    return is_torch_xla_available() and _is_package_available("torch_neuronx")[0]

