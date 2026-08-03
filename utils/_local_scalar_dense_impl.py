from typing import Any

def _local_scalar_dense_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> complex:
    x, y = split_complex_tensor(self)
    u = aten._local_scalar_dense(x, *args, **kwargs)
    v = aten._local_scalar_dense(y, *args, **kwargs)
    return complex(u, v)

