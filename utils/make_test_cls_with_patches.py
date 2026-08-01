
def make_test_cls_with_patches(
    cls: type,
    cls_prefix: str,
    fn_suffix: str,
    *patches: Any,
    xfail_prop: str | None = None,
    decorator: Callable[[Callable[..., Any]], Callable[..., Any]] = lambda x: x,
) -> type:
    DummyTestClass = type(f"{cls_prefix}{cls.__name__}", cls.__bases__, {})
    DummyTestClass.__qualname__ = DummyTestClass.__name__

    for name in dir(cls):
        if name.startswith("test_"):
            fn = getattr(cls, name)
            if not callable(fn):
                setattr(DummyTestClass, name, getattr(cls, name))
                continue
            new_name = f"{name}{fn_suffix}"
            new_fn = _make_fn_with_patches(fn, *patches)
            new_fn.__name__ = new_name
            if xfail_prop is not None and hasattr(fn, xfail_prop):
                new_fn = unittest.expectedFailure(new_fn)
            setattr(DummyTestClass, new_name, decorator(new_fn))
        # NB: Doesn't handle slots correctly, but whatever
        elif not hasattr(DummyTestClass, name):
            setattr(DummyTestClass, name, getattr(cls, name))

    return DummyTestClass

