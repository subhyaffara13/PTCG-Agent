
def _find_or_create_fake_mode() -> FakeTensorMode:
    from torch.fx.experimental.symbolic_shapes import ShapeEnv

    fake_mode = torch._guards.detect_fake_mode()
    if fake_mode is None:
        fake_mode = FakeTensorMode(shape_env=ShapeEnv())

    return fake_mode

