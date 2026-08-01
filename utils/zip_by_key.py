
def zip_by_key(a: dict[TK, TVa], b: dict[TK, TVb]) -> Iterator[tuple[TK, TVa, TVb]]:
    for arg, value in a.items():
        if arg in b:
            yield arg, value, b[arg]

