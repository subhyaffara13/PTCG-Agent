
def _format_args(
    args, defaults=None, annotations=None, skippable_names: set[str] | None = None
) -> str:
    if skippable_names is None:
        skippable_names = set()
    values = []
    if args is None:
        return ""
    if annotations is None:
        annotations = []
    if defaults is not None:
        default_offset = len(args) - len(defaults)
    else:
        default_offset = None
    packed = itertools.zip_longest(args, annotations)
    for i, (arg, annotation) in enumerate(packed):
        if arg.name in skippable_names:
            continue
        if isinstance(arg, Tuple):
            values.append(f"({_format_args(arg.elts)})")
        else:
            argname = arg.name
            default_sep = "="
            if annotation is not None:
                argname += ": " + annotation.as_string()
                default_sep = " = "
            values.append(argname)

            if default_offset is not None and i >= default_offset:
                if defaults[i - default_offset] is not None:
                    values[-1] += default_sep + defaults[i - default_offset].as_string()
    return ", ".join(values)

