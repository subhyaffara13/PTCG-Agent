
def make_instance(cls, args, kwargs):
    return cls(*args, **kwargs)


def make_instance(
    cls: Callable[..., T], args: Sequence[Any], kwargs: dict[str, Any]
) -> T:
    inst = cls(*args, **kwargs)
    inst._determine_worker()  # type: ignore[attr-defined]
    return inst


def make_instance(cls, args, kwargs, instance_state):
    fs = cls(*args, **kwargs)
    for attr, state_value in instance_state.items():
        setattr(fs, attr, state_value)
    return fs

