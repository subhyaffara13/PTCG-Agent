
def nested(
    *contexts: contextlib.AbstractContextManager[Any],
) -> Generator[tuple[contextlib.AbstractContextManager[Any], ...], None, None]:
    with contextlib.ExitStack() as stack:
        for ctx in contexts:
            stack.enter_context(ctx)
        yield contexts

