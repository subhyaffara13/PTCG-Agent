
def delete_model(ctx: click.Context, model_id: str) -> None:
    """Delete a model from the proxy"""
    client = create_client(ctx)
    result = client.models.delete(model_id=model_id)
    rich.print_json(data=result)

