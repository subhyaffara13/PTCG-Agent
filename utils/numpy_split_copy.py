from typing import List

def numpy_split_copy(x: Tensor, splits: Sequence[int], dim: int) -> List[Tensor]:
    x_np = to_numpy(x)
    arrs = np.split(x_np, splits, axis=dim)
    return [torch.tensor(arr, device=x.device, dtype=x.dtype) for arr in arrs]

