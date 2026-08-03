from typing import Any

def get_mypyc_attrs(
    stmt: ClassDef | Decorator, path: str, errors: Errors
) -> tuple[MypycAttrs, dict[MypycAttr, int]]:
    """Collect all the mypyc_attr attributes on a class definition or a function."""
    attrs: MypycAttrs = {}
    lines: dict[MypycAttr, int] = {}

    def set_mypyc_attr(key: str, value: Any, line: int) -> None:
        if key in MYPYC_ATTRS:
            attrs[key] = value
            lines[key] = line
        else:
            errors.error(f'"{key}" is not a supported "mypyc_attr"', path, line)
            supported_keys = '", "'.join(sorted(MYPYC_ATTRS))
            errors.note(f'supported keys: "{supported_keys}"', path, line)

    for dec in stmt.decorators:
        if d := get_mypyc_attr_call(dec):
            line = d.line
            for name, arg in zip(d.arg_names, d.args):
                if name is None:
                    if isinstance(arg, StrExpr):
                        set_mypyc_attr(arg.value, True, line)
                    else:
                        errors.error(
                            'All "mypyc_attr" positional arguments must be string literals.',
                            path,
                            line,
                        )
                else:
                    arg_value = get_mypyc_attr_literal(arg)
                    set_mypyc_attr(name, arg_value, line)

    return attrs, lines

