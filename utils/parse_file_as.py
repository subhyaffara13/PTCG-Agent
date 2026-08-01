
def parse_file_as(
    type_: Type[T],
    path: Union[str, Path],
    *,
    content_type: str = None,
    encoding: str = 'utf8',
    proto: Protocol = None,
    allow_pickle: bool = False,
    json_loads: Callable[[str], Any] = json.loads,
    type_name: Optional[NameFactory] = None,
) -> T:
    obj = load_file(
        path,
        proto=proto,
        content_type=content_type,
        encoding=encoding,
        allow_pickle=allow_pickle,
        json_loads=json_loads,
    )
    return parse_obj_as(type_, obj, type_name=type_name)

