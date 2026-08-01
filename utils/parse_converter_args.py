
def parse_converter_args(argstr: str) -> tuple[tuple[t.Any, ...], dict[str, t.Any]]:
    argstr += ","
    args = []
    kwargs = {}
    position = 0

    for item in _converter_args_re.finditer(argstr):
        if item.start() != position:
            raise ValueError(
                f"Cannot parse converter argument '{argstr[position : item.start()]}'"
            )

        value = item.group("stringval")
        if value is None:
            value = item.group("value")
        value = _pythonize(value)
        if not item.group("name"):
            args.append(value)
        else:
            name = item.group("name")
            kwargs[name] = value
        position = item.end()

    return tuple(args), kwargs

