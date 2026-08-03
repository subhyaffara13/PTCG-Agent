import itertools

def _extract_shape_env_and_assert_equal(
    args: tuple[object, ...] | list[object], kwargs: dict[str, object]
) -> ShapeEnv | None:
    from torch.fx.experimental.symbolic_shapes import is_symbolic, ShapeEnv, SymTypes

    def assert_equal(old: ShapeEnv | None, new: ShapeEnv) -> ShapeEnv:
        if old is not None:
            if old is not new:
                raise AssertionError("call with different ShapeEnv")
        return new

    shape_env = None
    for val in itertools.chain(args, kwargs.values()):
        if isinstance(val, ShapeEnv):
            shape_env = assert_equal(shape_env, val)
        if isinstance(val, SymTypes) and is_symbolic(val):
            shape_env = assert_equal(shape_env, val.node.shape_env)

    return shape_env

