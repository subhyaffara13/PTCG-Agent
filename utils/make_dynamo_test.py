
def make_dynamo_test(
    fn: Callable[..., Any] | None = None
) -> Callable[..., Any]:
    """
    Decorator function to create a dynamo test case. A function annotate with
    this decorator takes as input a unittest object.
    """
    from torch._dynamo.testing import CompileCounter, reset, optimize_assert
    if fn is None:
        return lambda fn: make_dynamo_test(fn)

    def standard_test(
        self: Any,
        fn: Callable[..., Any],
        kwargs,
    ) -> None:
        def dummy() -> None:
            fn(self, **kwargs)

        actual = CompileCounter()

        dummy()
        reset()
        opt_fn = optimize_assert(actual)(dummy)
        opt_fn()
        reset()

    @functools.wraps(fn)
    def test_fn(self: Any, **kwargs) -> None:
        return standard_test(
            self,
            fn=fn,
            kwargs=kwargs,
        )

    return test_fn

