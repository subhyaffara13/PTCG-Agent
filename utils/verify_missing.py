
def verify_missing(
    stub: Missing, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if runtime is MISSING:
        return
    yield Error(object_path, "is not present in stub", stub, runtime)

