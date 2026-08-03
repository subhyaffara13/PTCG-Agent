from typing import Any

def get_external_object_by_index(index: int) -> Any:
    assert index in index_to_external_object_weakref, (
        "Index not registered in index_to_user_object_weakref"
    )
    obj = index_to_external_object_weakref[index]()
    assert obj is not None, "User object is no longer alive"
    return index_to_external_object_weakref[index]()

