
def require_tensorboard(test_case):
    """
    Decorator for `tensorboard` dependency
    """
    return unittest.skipUnless(is_tensorboard_available(), "test requires tensorboard")

