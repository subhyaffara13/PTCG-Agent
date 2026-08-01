
def _clone_input(value: Any, fake_mode: FakeTensorMode | None) -> Any:
    if isinstance(value, torch.Tensor):
        # tensor subclasses will not be converted to FakeTensors and need to be cloned
        if not (
            isinstance(value, FakeTensor)
            or (
                # Is functional tensor fakeified by this instance of Dynamo
                torch._is_functional_tensor(value)
                and maybe_get_fake_mode(value) is fake_mode
            )
            or value.is_nested
        ):
            # NB: ensure strides are preserved
            value = clone_input(value)

    return value

