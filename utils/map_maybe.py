
def mapMaybe(func: Callable[[T], S | None], xs: Iterable[T]) -> Iterator[S]:
    for x in xs:
        r = func(x)
        if r is not None:
            yield r

