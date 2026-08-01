
def get_models_info(
    ctx: click.Context, output_format: Literal["table", "json"], columns: str
) -> None:
    """Get detailed information about all models"""
    client = create_client(ctx)
    models_info = client.models.info()
    assert isinstance(models_info, list)

    if output_format == "json":
        rich.print_json(data=models_info)
    else:  # table format
        table = rich.table.Table(title="Models Information")

        # Define all possible columns with their configurations
        column_configs: dict[str, dict[str, Any]] = {
            "public_model": {
                "header": "Public Model",
                "style": "cyan",
                "get_value": lambda m: str(m.get("model_name", "")),
            },
            "upstream_model": {
                "header": "Upstream Model",
                "style": "green",
                "get_value": lambda m: str(
                    m.get("litellm_params", {}).get("model", "")
                ),
            },
            "credential_name": {
                "header": "Credential Name",
                "style": "yellow",
                "get_value": lambda m: str(
                    m.get("litellm_params", {}).get("litellm_credential_name", "")
                ),
            },
            "created_at": {
                "header": "Created At",
                "style": "magenta",
                "get_value": lambda m: format_iso_datetime_str(
                    m.get("model_info", {}).get("created_at")
                ),
            },
            "updated_at": {
                "header": "Updated At",
                "style": "magenta",
                "get_value": lambda m: format_iso_datetime_str(
                    m.get("model_info", {}).get("updated_at")
                ),
            },
            "id": {
                "header": "ID",
                "style": "blue",
                "get_value": lambda m: str(m.get("model_info", {}).get("id", "")),
            },
            "input_cost": {
                "header": "Input Cost",
                "style": "green",
                "justify": "right",
                "get_value": lambda m: format_cost_per_1k_tokens(
                    m.get("model_info", {}).get("input_cost_per_token")
                ),
            },
            "output_cost": {
                "header": "Output Cost",
                "style": "green",
                "justify": "right",
                "get_value": lambda m: format_cost_per_1k_tokens(
                    m.get("model_info", {}).get("output_cost_per_token")
                ),
            },
        }

        # Add requested columns
        requested_columns = [col.strip() for col in columns.split(",")]
        for col_name in requested_columns:
            if col_name in column_configs:
                config = column_configs[col_name]
                table.add_column(
                    config["header"],
                    style=config["style"],
                    justify=config.get("justify", "left"),
                )
            else:
                click.echo(f"Warning: Unknown column '{col_name}'", err=True)

        # Add rows with only the requested columns
        for model in models_info:
            row_values = []
            for col_name in requested_columns:
                if col_name in column_configs:
                    row_values.append(column_configs[col_name]["get_value"](model))
            if row_values:
                table.add_row(*row_values)

        rich.print(table)

