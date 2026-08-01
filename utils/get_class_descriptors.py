
def get_class_descriptors(cls: type[object]) -> Sequence[str]:
    import inspect  # Lazy import for minor startup speed win

    # Maintain a cache of type -> attributes defined by descriptors in the class
    # (that is, attributes from __slots__ and C extension classes)
    if cls not in fields_cache:
        members = inspect.getmembers(
            cls, lambda o: inspect.isgetsetdescriptor(o) or inspect.ismemberdescriptor(o)
        )
        fields_cache[cls] = [x for x, y in members if x != "__weakref__" and x != "__dict__"]
    return fields_cache[cls]

