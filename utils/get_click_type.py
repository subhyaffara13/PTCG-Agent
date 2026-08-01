
def get_click_type(
    *, annotation: Any, parameter_info: ParameterInfo
) -> click.ParamType:
    if parameter_info.click_type is not None:
        return parameter_info.click_type

    elif parameter_info.parser is not None:
        return click.types.FuncParamType(parameter_info.parser)

    elif annotation is str:
        return click.STRING
    elif annotation is int:
        if parameter_info.min is not None or parameter_info.max is not None:
            min_ = None
            max_ = None
            if parameter_info.min is not None:
                min_ = int(parameter_info.min)
            if parameter_info.max is not None:
                max_ = int(parameter_info.max)
            return click.IntRange(min=min_, max=max_, clamp=parameter_info.clamp)
        else:
            return click.INT
    elif annotation is float:
        if parameter_info.min is not None or parameter_info.max is not None:
            return click.FloatRange(
                min=parameter_info.min,
                max=parameter_info.max,
                clamp=parameter_info.clamp,
            )
        else:
            return click.FLOAT
    elif annotation is bool:
        return click.BOOL
    elif annotation == UUID:
        return click.UUID
    elif annotation == datetime:
        return click.DateTime(formats=parameter_info.formats)
    elif (
        annotation == Path
        or parameter_info.allow_dash
        or parameter_info.path_type
        or parameter_info.resolve_path
    ):
        return TyperPath(
            exists=parameter_info.exists,
            file_okay=parameter_info.file_okay,
            dir_okay=parameter_info.dir_okay,
            writable=parameter_info.writable,
            readable=parameter_info.readable,
            resolve_path=parameter_info.resolve_path,
            allow_dash=parameter_info.allow_dash,
            path_type=parameter_info.path_type,
        )
    elif lenient_issubclass(annotation, FileTextWrite):
        return click.File(
            mode=parameter_info.mode or "w",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, FileText):
        return click.File(
            mode=parameter_info.mode or "r",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, FileBinaryRead):
        return click.File(
            mode=parameter_info.mode or "rb",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, FileBinaryWrite):
        return click.File(
            mode=parameter_info.mode or "wb",
            encoding=parameter_info.encoding,
            errors=parameter_info.errors,
            lazy=parameter_info.lazy,
            atomic=parameter_info.atomic,
        )
    elif lenient_issubclass(annotation, Enum):
        # The custom TyperChoice is only needed for Click < 8.2.0, to parse the
        # command line values matching them to the enum values. Click 8.2.0 added
        # support for enum values but reading enum names.
        # Passing here the list of enum values (instead of just the enum) accounts for
        # Click < 8.2.0.
        return TyperChoice(
            [item.value for item in annotation],
            case_sensitive=parameter_info.case_sensitive,
        )
    elif is_literal_type(annotation):
        return click.Choice(
            literal_values(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    raise RuntimeError(f"Type not yet supported: {annotation}")  # pragma: no cover

