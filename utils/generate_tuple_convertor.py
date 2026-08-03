from typing import Any, Callable

def generate_tuple_convertor(
    types: Sequence[Any],
) -> Callable[[tuple[Any, ...] | None], tuple[Any, ...] | None]:
    convertors = [determine_type_convertor(type_) for type_ in types]

    def internal_convertor(
        param_args: tuple[Any, ...] | None,
    ) -> tuple[Any, ...] | None:
        if param_args is None:
            return None
        return tuple(
            convertor(arg) if convertor else arg
            for (convertor, arg) in zip(convertors, param_args, strict=False)
        )

    return internal_convertor

