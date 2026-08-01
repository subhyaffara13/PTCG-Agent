
def invalid_removeable_handle() -> RemovableHandle:
    # need a subclass so weakref works
    class Invalid(dict):  # type: ignore[type-arg]
        pass

    return RemovableHandle(Invalid())

