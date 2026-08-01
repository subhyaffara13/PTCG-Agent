
def maybe_profile(should_profile: bool, *args: Any, **kwargs: Any) -> Iterator[Any]:
    if should_profile:
        with torch.profiler.profile(*args, **kwargs) as p:
            yield p
    else:
        yield

