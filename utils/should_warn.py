
def should_warn(key: t.Any) -> bool:
    """Add our own checks for too many deprecation warnings.

    Limit to once per package.
    """
    env_flag = os.environ.get("TRAITLETS_ALL_DEPRECATIONS")
    if env_flag and env_flag != "0":
        return True

    if key not in _deprecations_shown:
        _deprecations_shown.add(key)
        return True
    else:
        return False


def should_warn(*args):
    not_mono = not any(map(operator.attrgetter("is_monotonic_increasing"), args))
    only_one_dt = reduce(
        operator.xor, (issubclass(x.dtype.type, np.datetime64) for x in args)
    )
    return not_mono and only_one_dt

