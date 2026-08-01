
def path_wrapper(func):
    """Return the given infer function wrapped to handle the path.

    Used to stop inference if the node has already been looked
    at for a given `InferenceContext` to prevent infinite recursion
    """

    @functools.wraps(func)
    def wrapped(
        node, context: InferenceContext | None = None, _func=func, **kwargs
    ) -> Generator:
        """Wrapper function handling context."""
        if context is None:
            context = InferenceContext()
        if context.push(node):
            return

        yielded = set()

        for res in _func(node, context, **kwargs):
            # unproxy only true instance, not const, tuple, dict...
            if res.__class__.__name__ == "Instance":
                ares = res._proxied
            else:
                ares = res
            if ares not in yielded:
                yield res
                yielded.add(ares)

    return wrapped

