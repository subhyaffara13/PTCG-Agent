
def list_models(ctx: click.Context, output_format: Literal["table", "json"]) -> None:
    """List all available models"""
    client = create_client(ctx)
    models_list = client.models.list()
    assert isinstance(models_list, list)

    if output_format == "json":
        rich.print_json(data=models_list)
    else:  # table format
        table = rich.table.Table(title="Available Models")

        # Add columns based on the data structure
        table.add_column("ID", style="cyan")
        table.add_column("Object", style="green")
        table.add_column("Created", style="magenta")
        table.add_column("Owned By", style="yellow")

        # Add rows
        for model in models_list:
            created = model.get("created")
            # Convert string timestamp to integer if needed
            if isinstance(created, str) and created.isdigit():
                created = int(created)

            table.add_row(
                str(model.get("id", "")),
                str(model.get("object", "model")),
                (
                    format_timestamp(created)
                    if isinstance(created, int)
                    else format_iso_datetime_str(created)
                ),
                str(model.get("owned_by", "")),
            )

        rich.print(table)

