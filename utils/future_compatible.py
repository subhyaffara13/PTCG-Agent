
def future_compatible(fn: CallableT) -> CallableT:
    """Wrap a method of `HfApi` to handle `run_as_future=True`.

    A method flagged as "future_compatible" will be called in a thread if `run_as_future=True` and return a
    `concurrent.futures.Future` instance. Otherwise, it will be called normally and return the result.
    """
    sig = inspect.signature(fn)
    args_params = list(sig.parameters)[1:]  # remove "self" from list

    @wraps(fn)
    def _inner(self, *args, **kwargs):
        # Get `run_as_future` value if provided (default to False)
        if "run_as_future" in kwargs:
            run_as_future = kwargs["run_as_future"]
            kwargs["run_as_future"] = False  # avoid recursion error
        else:
            run_as_future = False
            for param, value in zip(args_params, args):
                if param == "run_as_future":
                    run_as_future = value
                    break

        # Call the function in a thread if `run_as_future=True`
        if run_as_future:
            return self.run_as_future(fn, self, *args, **kwargs)

        # Otherwise, call the function normally
        return fn(self, *args, **kwargs)

    _inner.is_future_compatible = True  # type: ignore
    return _inner  # type: ignore

