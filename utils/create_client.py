
def create_client(ctx: click.Context) -> Client:
    """Helper function to create a client from context."""
    return Client(base_url=ctx.obj["base_url"], api_key=ctx.obj["api_key"])

