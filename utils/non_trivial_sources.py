
def non_trivial_sources(op: Op) -> set[Value]:
    result = set()
    for source in op.sources():
        if not isinstance(source, (Integer, Float, Undef)):
            result.add(source)
    return result

