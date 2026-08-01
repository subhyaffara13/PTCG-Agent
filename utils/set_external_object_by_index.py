
def set_external_object_by_index(index: int, value: Any) -> None:
    """Update an entry in the external object registry at runtime."""
    keep_alive.append(value)
    index_to_external_object_weakref[index] = weakref.ref(value)

