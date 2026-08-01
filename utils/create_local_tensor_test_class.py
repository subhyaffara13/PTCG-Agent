
def create_local_tensor_test_class(
    orig_cls, skipped_tests=None, base_class=LocalDTensorTestBase
):
    if skipped_tests is None:
        skipped_tests = []

    dct = orig_cls.__dict__.copy()
    for name in list(dct.keys()):
        fn = dct[name]
        if not callable(fn):
            continue
        elif name in skipped_tests:
            dct[name] = lambda self: self.skipTest("Skipped test")
        elif name.startswith("test_"):
            ctxs = [
                lambda test: test._get_local_tensor_mode(),
            ]
            dct[name] = make_wrapped(fn, ctxs)

    cls = type(
        orig_cls.__name__ + "WithLocalTensor",
        (base_class,) + orig_cls.__bases__,
        dct,
    )
    cls.__file__ = __file__
    return cls

