
def _clear_fake_mode_weakrefs(
    fake_mode: torch._subclasses.fake_tensor.FakeTensorMode | None,
) -> None:
    """Clear WeakIdRef entries from a FakeTensorMode's describer."""
    if fake_mode is None:
        return
    describer = fake_mode.fake_tensor_converter.meta_converter.describer
    describer.lookup_tensor.clear()
    describer.lookup_storage.clear()

