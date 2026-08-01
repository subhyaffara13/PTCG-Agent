
def get_edges(o: object) -> Iterator[tuple[object, object]]:
    for s, e in get_edge_candidates(o):
        if isinstance(e, FUNCTION_TYPES):
            # We don't want to collect methods, but do want to collect values
            # in closures and self pointers to other objects

            if hasattr(e, "__closure__"):
                yield (s, "__closure__"), e.__closure__
            if hasattr(e, "__self__"):
                se = e.__self__
                if se is not o and se is not type(o) and hasattr(s, "__self__"):
                    yield s.__self__, se
        else:
            if type(e) not in TYPE_BLACKLIST:
                yield s, e

