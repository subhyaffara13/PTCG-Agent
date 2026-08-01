
def generate_list_convertor(
    convertor: Callable[[Any], Any] | None, default_value: Any | None
) -> Callable[[Sequence[Any] | None], list[Any] | None]:
    def internal_convertor(value: Sequence[Any] | None) -> list[Any] | None:
        if (value is None) or (default_value is None and len(value) == 0):
            return None
        return [convertor(v) if convertor else v for v in value]

    return internal_convertor

