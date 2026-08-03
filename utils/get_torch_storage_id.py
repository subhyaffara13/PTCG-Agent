from typing import Any

def get_torch_storage_id(tensor: "torch.Tensor") -> tuple["torch.device", int | tuple[Any, ...], int] | None:
    """
    Return unique identifier to a tensor storage.

    Multiple different tensors can share the same underlying storage. This identifier is
    guaranteed to be unique and constant for this tensor's storage during its lifetime. Two tensor storages with
    non-overlapping lifetimes may have the same id.
    In the case of meta tensors, we return None since we can't tell if they share the same storage.

    Taken from https://github.com/huggingface/transformers/blob/1ecf5f7c982d761b4daaa96719d162c324187c64/src/transformers/pytorch_utils.py#L278.
    """
    if tensor.device.type == "meta":
        return None
    else:
        return tensor.device, _get_unique_id(tensor), get_torch_storage_size(tensor)

