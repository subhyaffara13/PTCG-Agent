
def unset(ctx: click.Context, key: Any) -> None:
    """
    Removes the given key.

    This doesn't follow symlinks, to avoid accidentally modifying a file at a
    potentially untrusted path.
    """
    file = ctx.obj["FILE"]
    quote = ctx.obj["QUOTE"]
    success, key = unset_key(file, key, quote)
    if success:
        click.echo(f"Successfully removed {key}")
    else:
        sys.exit(1)

