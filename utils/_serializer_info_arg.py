
def _serializer_info_arg(mode: Literal['plain', 'wrap'], n_positional: int) -> bool | None:
    if mode == 'plain':
        if n_positional == 1:
            # (input_value: Any, /) -> Any
            return False
        elif n_positional == 2:
            # (model: Any, input_value: Any, /) -> Any
            return True
    else:
        assert mode == 'wrap', f"invalid mode: {mode!r}, expected 'plain' or 'wrap'"
        if n_positional == 2:
            # (input_value: Any, serializer: SerializerFunctionWrapHandler, /) -> Any
            return False
        elif n_positional == 3:
            # (input_value: Any, serializer: SerializerFunctionWrapHandler, info: SerializationInfo, /) -> Any
            return True

    return None

