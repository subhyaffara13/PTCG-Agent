
def check_dynamic_shape_capture() -> bool:
    # This also mirrors config from `test/dynamo/test_dynamic_shapes.py:make_dynamic_cls`
    return not config.assume_static_by_default

