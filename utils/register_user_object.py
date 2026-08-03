from typing import Any

def register_user_object(value: Any, source: Source) -> int:
    global index_to_bytecode_constructor
    index = len(index_to_bytecode_constructor)
    index_to_bytecode_constructor[index] = lambda cg: cg(source)
    try:
        index_to_external_object_weakref[index] = weakref.ref(value)
    except TypeError as e:
        from .exc import unimplemented

        unimplemented(
            gb_type="Failed to make weakref to User Object",
            context=f"user_object: {value}",
            explanation="Object does not allow us to make a weakref to it",
            hints=[],
            from_exc=e,
        )
    return index

