
def AddModel(builder, model):
    InferenceSessionAddModel(builder, model)


def add_model(
    ctx: click.Context, model_name: str, param: tuple[str, ...], info: tuple[str, ...]
) -> None:
    """Add a new model to the proxy"""
    # Convert parameters from key=value format to dict
    model_params = dict(p.split("=", 1) for p in param)
    model_info = dict(i.split("=", 1) for i in info) if info else None

    client = create_client(ctx)
    result = client.models.new(
        model_name=model_name,
        model_params=model_params,
        model_info=model_info,
    )
    rich.print_json(data=result)

