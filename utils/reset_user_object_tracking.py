
def reset_user_object_tracking() -> None:
    index_to_bytecode_constructor.clear()
    index_to_external_object_weakref.clear()
    keep_alive.clear()

