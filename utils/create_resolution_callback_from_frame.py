
def createResolutionCallbackFromFrame(frames_up: int = 0) -> Callable[[str], Any]:
    """
    Creates a function which, given a string variable name,
    returns the value of the variable in the scope of the caller of
    the function which called createResolutionCallbackFromFrame (by default).

    This is used to enable access in-scope Python variables inside
    TorchScript fragments.

    frames_up is number of additional frames to go up on the stack.
    The default value is 0, which correspond to the frame of the caller
    of createResolutionCallbackFromFrame. Also for example, if frames_up is set
    to 1, then the frame of the caller's caller of createResolutionCallbackFromFrame
    will be taken.

    For example, the following program prints 2::

        def bar():
            cb = createResolutionCallbackFromFrame(1)
            print(cb("foo"))


        def baz():
            foo = 2
            bar()


        baz()
    """
    frame = inspect.currentframe()
    i = 0
    while i < frames_up + 1:
        if frame is None:
            raise AssertionError(f"frame is None at iteration {i}")
        frame = frame.f_back
        i += 1

    if frame is None:
        raise AssertionError("frame is None after traversing frames_up")
    f_locals = frame.f_locals
    f_globals = frame.f_globals

    class env:
        def __getattr__(self, key: str) -> Any:
            if key in f_locals:
                return f_locals[key]
            elif key in f_globals:
                return f_globals[key]
            elif key in dir(builtins):
                return getattr(builtins, key)

    return createResolutionCallbackFromEnv(env())

