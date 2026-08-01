
def normalize_callables(s: ProperType, t: ProperType) -> tuple[ProperType, ProperType]:
    if isinstance(s, (CallableType, Overloaded)):
        s = s.with_unpacked_kwargs()
    if isinstance(t, (CallableType, Overloaded)):
        t = t.with_unpacked_kwargs()
    return s, t

