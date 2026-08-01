
def find_recursive_objects(objs: list[object]) -> None:
    """Find additional objects referenced by objs and append them to objs.

    We use this since gc.get_objects() does not return objects without pointers
    in them such as strings.
    """
    seen = {id(o) for o in objs}

    def visit(o: object) -> None:
        if id(o) not in seen:
            objs.append(o)
            seen.add(id(o))

    for obj in objs.copy():
        if type(obj) is FakeInfo:
            # Processing these would cause a crash.
            continue
        if type(obj) in (dict, defaultdict):
            for key, val in cast(dict[object, object], obj).items():
                visit(key)
                visit(val)
        if type(obj) in (list, tuple, set):
            for x in cast(Iterable[object], obj):
                visit(x)
        if hasattr(obj, "__slots__"):
            for base in type.mro(type(obj)):
                for slot in getattr(base, "__slots__", ()):
                    if hasattr(obj, slot):
                        visit(getattr(obj, slot))

