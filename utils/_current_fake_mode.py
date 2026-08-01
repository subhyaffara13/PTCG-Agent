
def _current_fake_mode() -> FakeTensorMode:
    fake_mode = None
    if context := torch._guards.TracingContext.try_get():
        fake_mode = context.fake_mode
    if fake_mode is not None:
        return fake_mode

    shape_env = torch.fx.experimental.symbolic_shapes.ShapeEnv()
    return FakeTensorMode(shape_env=shape_env)

