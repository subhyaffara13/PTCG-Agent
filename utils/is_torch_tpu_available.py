
def is_torch_tpu_available(check_device: bool = False) -> bool:
    import torch

    if importlib.util.find_spec("torch_tpu") is None:
        return False

    if check_device:
        try:
            import torch_tpu  # noqa: F401

            if hasattr(torch, "tpu") and torch.tpu.is_available():
                return torch.tpu.device_count() >= 1
            return False
        except RuntimeError:
            return False

    return hasattr(torch, "tpu") and torch.tpu.is_available()


def is_torch_tpu_available(check_device=True):
    """
    Checks if `torch_xla` is installed and potentially if a TPU is in the environment

    Taken from https://github.com/huggingface/transformers/blob/1ecf5f7c982d761b4daaa96719d162c324187c64/src/transformers/utils/import_utils.py#L463.
    """
    if importlib.util.find_spec("torch_xla") is not None:
        if check_device:
            # We need to check if `xla_device` can be found, will raise a RuntimeError if not
            try:
                import torch_xla.core.xla_model as xm  # type: ignore[import]

                _ = xm.xla_device()
                return True
            except RuntimeError:
                return False
        return True
    return False

