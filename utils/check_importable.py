
def check_importable(dist, attr, value):
    try:
        ep = metadata.EntryPoint(value=value, name=None, group=None)
        assert not ep.extras
    except (TypeError, ValueError, AttributeError, AssertionError) as e:
        raise DistutilsSetupError(
            f"{attr!r} must be importable 'module:attrs' string (got {value!r})"
        ) from e

