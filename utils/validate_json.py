
def validate_json(
    ctx: click.Context,
    param: click.Option | click.Parameter,
    value: typing.Any,
) -> typing.Any:
    if value is None:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:  # pragma: no cover
        raise click.BadParameter("Not valid JSON")


def validate_json(v: Any, config: 'BaseConfig') -> Any:
    if v is None:
        # pass None through to other validators
        return v
    try:
        return config.json_loads(v)  # type: ignore
    except ValueError:
        raise errors.JsonError()
    except TypeError:
        raise errors.JsonTypeError()

