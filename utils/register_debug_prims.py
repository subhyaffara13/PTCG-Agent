
def register_debug_prims() -> None:
    torch.library.define(
        "debugprims::load_tensor",
        "(str name, int[] size, int[] stride, *, ScalarType dtype, Device device) -> Tensor",
    )

    @torch.library.impl("debugprims::load_tensor", "BackendSelect")
    def load_tensor_factory(
        name: str,
        size: Sequence[int],
        stride: Sequence[int],
        dtype: torch.dtype,
        device: torch.device,
    ) -> torch.Tensor:
        if LOAD_TENSOR_READER is None:
            from torch._dynamo.testing import rand_strided

            return rand_strided(size, stride, dtype, device)
        else:
            from torch._dynamo.utils import clone_input

            # device argument here takes care of coercion
            r = LOAD_TENSOR_READER.read_tensor(name, device=device)
            if list(r.size()) != size:
                raise AssertionError(f"{r.size()} != {size}")
            if list(r.stride()) != stride:
                raise AssertionError(f"{r.stride()} != {stride}")
            if r.device != device:
                raise AssertionError(f"{r.device} != {device}")

            # Unlike the other properties, we will do coercions for dtype
            # mismatch
            if r.dtype != dtype:
                r = clone_input(r, dtype=dtype)  # type: ignore[no-untyped-call]
            return r

