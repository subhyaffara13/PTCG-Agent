
def update_model(
    ctx: click.Context, model_id: str, param: tuple[str, ...], info: tuple[str, ...]
) -> None:
    """Update an existing model's configuration"""
    # Convert parameters from key=value format to dict
    model_params = dict(p.split("=", 1) for p in param)
    model_info = dict(i.split("=", 1) for i in info) if info else None

    client = create_client(ctx)
    result = client.models.update(
        model_id=model_id,
        model_params=model_params,
        model_info=model_info,
    )
    rich.print_json(data=result)

