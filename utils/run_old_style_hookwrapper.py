
def run_old_style_hookwrapper(
    hook_impl: HookImpl, hook_name: str, args: Sequence[object]
) -> Teardown:
    """
    backward compatibility wrapper to run a old style hookwrapper as a wrapper
    """

    teardown: Teardown = cast(Teardown, hook_impl.function(*args))
    try:
        next(teardown)
    except StopIteration:
        _raise_wrapfail(teardown, "did not yield")
    try:
        res = yield
        result = Result(res, None)
    except BaseException as exc:
        result = Result(None, exc)
    try:
        teardown.send(result)
    except StopIteration:
        pass
    except BaseException as e:
        _warn_teardown_exception(hook_name, hook_impl, e)
        raise
    else:
        _raise_wrapfail(teardown, "has second yield")
    finally:
        teardown.close()
    return result.get_result()

