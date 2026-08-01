
def is_typeddict(type_: Type[Any]) -> bool:
    """
    Check if a given class is a typed dict (from `typing` or `typing_extensions`)
    In 3.10, there will be a public method (https://docs.python.org/3.10/library/typing.html#typing.is_typeddict)
    """
    from pydantic.v1.utils import lenient_issubclass

    return lenient_issubclass(type_, dict) and hasattr(type_, '__total__')


def is_typeddict(tp: Type[Any]) -> bool:
    return typing_extensions.is_typeddict(tp)

