
def list_values(ctx: click.Context, output_format: str) -> None:
    """Display all the stored key/value."""
    file = ctx.obj["FILE"]

    with stream_file(file) as stream:
        values = dotenv_values(stream=stream)

    if output_format == "json":
        click.echo(json.dumps(values, indent=2, sort_keys=True))
    else:
        prefix = "export " if output_format == "export" else ""
        for k in sorted(values):
            v = values[k]
            if v is not None:
                if output_format in ("export", "shell"):
                    v = shlex.quote(v)
                click.echo(f"{prefix}{k}={v}")

