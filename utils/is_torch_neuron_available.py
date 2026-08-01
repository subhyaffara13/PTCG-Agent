
def is_torch_neuron_available(check_device: bool = False) -> bool:
    import torch

    if importlib.util.find_spec("torch_neuronx") is None:
        return False

    if check_device:
        try:
            import torch_neuronx  # noqa: F401

            # Will raise a RuntimeError if no Neuron is found
            if hasattr(torch, "neuron"):
                _ = torch.neuron.device_count()
                return torch.neuron.is_available()
            return False
        except RuntimeError:
            return False

    return hasattr(torch, "neuron") and torch.neuron.is_available()

