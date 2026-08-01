
def _first_set(first: t.Union[t.Any, object], second: t.Any) -> t.Any:
    return second if first is _unset else first

