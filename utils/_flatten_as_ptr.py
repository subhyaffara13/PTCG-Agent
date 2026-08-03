from typing import Any, Dict, List

def _flatten_as_ptr(
    tensors: Dict[str, torch.Tensor], keep_alive_buffer: List
) -> Dict[str, Dict[str, Any]]:
    _evaluate_tensors_for_save(tensors)
    flattened = {}
    for k, v in tensors.items():
        # XXX: doing this check later on instead of in _evaluate_tensors_for_save
        # since on old versions of torch, SparseTensorImpl do not implement is_contiguous
        # and we do the sparsity check in _evaluate_tensors_for_save.
        if not v.is_contiguous():
            raise ValueError(
                f"You are trying to save a non contiguous tensor: `{k}` which is not allowed. It either means you"
                " are trying to save tensors which are reference of each other in which case it's recommended to save"
                " only the full tensors, and reslice at load time, or simply call `.contiguous()` on your tensor to"
                " pack it before saving."
            )
        arr, tensor_ref = _to_ndarray(v)
        keep_alive_buffer.append((arr, tensor_ref))
        flattened[k] = TensorSpec(
            dtype=str(v.dtype).split(".")[-1],
            shape=v.shape,
            data_ptr=arr.ctypes.data,
            data_len=arr.nbytes,
        )
    return flattened

