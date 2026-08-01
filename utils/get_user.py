
def get_user() -> str | None:
    """Return the current user name, or None if getuser() does not work
    in the current environment (see #1010)."""
    try:
        # In some exotic environments, getpass may not be importable.
        import getpass

        return getpass.getuser()
    except (ImportError, OSError, KeyError):
        return None


def get_user(ctx: click.Context, user_id: str):
    """Get information about a specific user"""
    client = UsersManagementClient(
        base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"]
    )
    result = client.get_user(user_id=user_id)
    rich.print_json(data=result)

