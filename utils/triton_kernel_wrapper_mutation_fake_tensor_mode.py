from typing import Any

def triton_kernel_wrapper_mutation_fake_tensor_mode(
    mode: FakeTensorMode,
    *,
    kernel_idx: int,
    constant_args_idx: int,
    grid: list["TritonGridType"],
    tma_descriptor_metadata: TMADescriptorMetadata,
    kwargs: dict[str, Any],
) -> None:
    with mode:
        return None

