
def delete_user(ctx: click.Context, user_ids):
    """Delete one or more users by user_id"""
    client = UsersManagementClient(
        base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"]
    )
    result = client.delete_user(list(user_ids))
    rich.print_json(data=result)

