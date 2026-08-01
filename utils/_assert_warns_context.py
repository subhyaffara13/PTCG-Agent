
def _assert_warns_context(warning_class, name=None):
    __tracebackhide__ = True  # Hide traceback for py.test
    with suppress_warnings() as sup:
        l = sup.record(warning_class)
        yield
        if not len(l) > 0:
            name_str = f" when calling {name}" if name is not None else ""
            raise AssertionError("No warning raised" + name_str)


def _assert_warns_context(warning_class, name=None):
    __tracebackhide__ = True  # Hide traceback for py.test
    with suppress_warnings(_warn=False) as sup:
        l = sup.record(warning_class)
        yield
        if not len(l) > 0:
            name_str = f' when calling {name}' if name is not None else ''
            raise AssertionError("No warning raised" + name_str)

