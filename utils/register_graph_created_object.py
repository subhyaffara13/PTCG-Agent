from typing import Any, Callable

def register_graph_created_object(
    example_value: Any, construct_fn: Callable[[int, PyCodegen], None]
) -> int:
    global index_to_bytecode_constructor
    global keep_alive
    keep_alive.append(example_value)
    index = len(index_to_bytecode_constructor)
    index_to_bytecode_constructor[index] = lambda cg: construct_fn(index, cg)
    try:
        index_to_external_object_weakref[index] = weakref.ref(example_value)
    except TypeError as e:
        from .exc import unimplemented

        unimplemented(
            gb_type="Failed to make weakref to graph-created external object",
            context=f"user_object: {example_value}",
            explanation="Object does not allow us to make a weakref to it",
            hints=[],
            from_exc=e,
        )
    return index

