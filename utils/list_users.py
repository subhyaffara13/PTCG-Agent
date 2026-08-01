
def list_users(ctx: click.Context):
    """List all users"""
    client = UsersManagementClient(
        base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"]
    )
    users = client.list_users()
    if isinstance(users, dict) and "users" in users:
        users = users["users"]
    if not users:
        click.echo("No users found.")
        return
    from rich.table import Table
    from rich.console import Console

    table = Table(title="Users")
    table.add_column("User ID", style="cyan")
    table.add_column("Email", style="green")
    table.add_column("Role", style="magenta")
    table.add_column("Teams", style="yellow")
    for user in users:
        table.add_row(
            str(user.get("user_id", "")),
            str(user.get("user_email", "")),
            str(user.get("user_role", "")),
            ", ".join(user.get("teams", []) or []),
        )
    console = Console()
    console.print(table)

