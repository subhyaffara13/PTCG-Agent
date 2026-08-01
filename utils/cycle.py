
def cycle(iterable: Iterable[_T]) -> Iterator[_T]:
    iterator = iter(iterable)

    def _cycle(iterator: Iterator[_T]) -> Iterator[_T]:
        # pyrefly: ignore [implicit-any]
        saved = []
        for element in iterable:
            yield element
            saved.append(element)

        while saved:
            for element in saved:
                yield element

    return _cycle(iterator)

