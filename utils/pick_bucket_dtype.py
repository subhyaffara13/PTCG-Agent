
def pick_bucket_dtype(dtypes: list[torch.dtype]) -> torch.dtype:  # type: ignore[name-defined]
    assert len(dtypes) > 0
    return min(dtypes, key=operator.attrgetter("itemsize"))

