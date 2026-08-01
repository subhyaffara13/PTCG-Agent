
def _create_dummy_tensor_from_layout(layout: Layout) -> torch.Tensor | None:
    """
    Create a FakeTensor from a Layout for kernel filtering.

    Uses Layout.get_example() which creates FakeTensors within V.fake_mode,
    avoiding real CUDA memory allocation. cutlass_api only needs shape/stride/dtype
    metadata for its supports() checks.
    """
    try:
        return layout.get_example()
    except Exception:
        return None

