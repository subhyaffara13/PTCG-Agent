
def create_user(ctx: click.Context, email, role, alias, team, max_budget):
    """Create a new user"""
    client = UsersManagementClient(
        base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"]
    )
    user_data = {
        "user_email": email,
        "user_role": role,
    }
    if alias:
        user_data["user_alias"] = alias
    if team:
        user_data["teams"] = list(team)
    if max_budget is not None:
        user_data["max_budget"] = max_budget
    result = client.create_user(user_data)
    rich.print_json(data=result)

