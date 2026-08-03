import functools
from typing import Callable

def construct_meta_kernel(qualname: str, fake_impl_holder: FakeImplHolder) -> Callable:
    if fake_impl_holder.kernel is None:
        raise AssertionError("fake_impl_holder.kernel must not be None")

    @functools.wraps(fake_impl_holder.kernel.func)
    def meta_kernel(*args, **kwargs):
        if fake_impl_holder.kernel is None:
            raise AssertionError("fake_impl_holder.kernel must not be None")
        source = fake_impl_holder.kernel.source

        def error_on_ctx():
            raise RuntimeError(
                f"{qualname} ({source}): You're trying to run this operator "
                f"with meta Tensors (as opposed to FakeTensors), but this "
                f"operator may return an output Tensor with data-dependent shape. Meta "
                f"Tensors don't support operators with outputs that have data-dependent shapes "
                f"but FakeTensors do. "
                f"If your operator does not return an output with data-dependent shape, "
                f"make sure the FakeTensor and/or meta kernel does not call "
                f"torch.library.get_ctx(). Otherwise, please use FakeTensors."
            )

        with set_ctx_getter(error_on_ctx):
            return fake_impl_holder.kernel(*args, **kwargs)

    return meta_kernel

