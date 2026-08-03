from typing import Any

def _sparse_coo_tensor_with_dims_and_tensors(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    return constructors(fake_mode, func, *args, **kwargs)


def _sparse_coo_tensor_with_dims_and_tensors(func, *args, **kwargs):
    new_args = list(args)
    if is_masked_tensor(args[-1]):
        new_args[-1] = args[-1].get_data()
    if is_masked_tensor(args[-2]):
        new_args[-2] = args[-2].get_data()

    new_data = func(*new_args, **kwargs)
    new_args[-1] = torch.ones_like(new_args[-1])
    new_mask = func(*new_args, **kwargs).bool()

    return MaskedTensor(new_data, new_mask)

