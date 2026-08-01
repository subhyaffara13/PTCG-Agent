
def assert_raises_fpe(strmatch, callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except FloatingPointError as exc:
        assert_(str(exc).find(strmatch) >= 0,
                f"Did not raise floating point {strmatch} error")
    else:
        assert_(False,
                f"Did not raise floating point {strmatch} error")

