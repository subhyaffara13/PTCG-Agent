
def determine_type_convertor(type_: Any) -> Callable[[Any], Any] | None:
    convertor: Callable[[Any], Any] | None = None
    if lenient_issubclass(type_, Path):
        convertor = param_path_convertor
    if lenient_issubclass(type_, Enum):
        convertor = generate_enum_convertor(type_)
    return convertor

