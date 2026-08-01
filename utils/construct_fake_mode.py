
def construct_fake_mode(
    flat_args: list[Any], aot_config: AOTConfig
) -> tuple[FakeTensorMode, ShapeEnv | None]:
    fake_mode = detect_fake_mode(flat_args)
    if fake_mode is None:
        shape_env = ShapeEnv() if aot_config.dynamic_shapes else None
        fake_mode = FakeTensorMode(shape_env=shape_env)
    else:
        shape_env = fake_mode.shape_env
    return (fake_mode, shape_env)

