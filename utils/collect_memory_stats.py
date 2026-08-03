import sys

def collect_memory_stats() -> tuple[dict[str, int], dict[str, int]]:
    """Return stats about memory use.

    Return a tuple with these items:
      - Dict from object kind to number of instances of that kind
      - Dict from object kind to total bytes used by all instances of that kind
    """
    objs = gc.get_objects()
    find_recursive_objects(objs)

    inferred = {}
    for obj in objs:
        if type(obj) is FakeInfo:
            # Processing these would cause a crash.
            continue
        n = type(obj).__name__
        if hasattr(obj, "__dict__"):
            # Keep track of which class a particular __dict__ is associated with.
            inferred[id(obj.__dict__)] = f"{n} (__dict__)"
        if isinstance(obj, (Node, Type)):  # type: ignore[misc]
            if hasattr(obj, "__dict__"):
                for x in obj.__dict__.values():
                    if isinstance(x, list):
                        # Keep track of which node a list is associated with.
                        inferred[id(x)] = f"{n} (list)"
                    if isinstance(x, tuple):
                        # Keep track of which node a list is associated with.
                        inferred[id(x)] = f"{n} (tuple)"

            for k in get_class_descriptors(type(obj)):
                x = getattr(obj, k, None)
                if isinstance(x, list):
                    inferred[id(x)] = f"{n} (list)"
                if isinstance(x, tuple):
                    inferred[id(x)] = f"{n} (tuple)"

    freqs: dict[str, int] = {}
    memuse: dict[str, int] = {}
    for obj in objs:
        if id(obj) in inferred:
            name = inferred[id(obj)]
        else:
            name = type(obj).__name__
        freqs[name] = freqs.get(name, 0) + 1
        memuse[name] = memuse.get(name, 0) + sys.getsizeof(obj)

    return freqs, memuse

