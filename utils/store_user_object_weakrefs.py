
def store_user_object_weakrefs(*args: Any) -> None:
    global index_to_external_object_weakref
    index_to_external_object_weakref.clear()
    index_to_external_object_weakref.update(
        {i: weakref.ref(arg) for i, arg in enumerate(args)}
    )

