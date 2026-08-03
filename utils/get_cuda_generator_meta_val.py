from typing import Any

def get_cuda_generator_meta_val(device_idx: int) -> Any:
    """
    Get a generator value to use as a meta val

    newly cloned generator will not contain tensors. it is only Generators that are
    registered to a CUDAGraph that contain tensors. since this does not contain Tensor
    it is fine to use in the meta.
    """
    return torch.cuda.default_generators[device_idx].clone_state()

