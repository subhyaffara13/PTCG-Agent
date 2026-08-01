
def validate_auth(
    ctx: click.Context,
    param: click.Option | click.Parameter,
    value: typing.Any,
) -> typing.Any:
    if value == (None, None):
        return None

    username, password = value
    if password == "-":  # pragma: no cover
        password = click.prompt("Password", hide_input=True)
    return (username, password)

