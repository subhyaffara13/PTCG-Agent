
def _print_models_table(added_models: list[ModelYamlInfo], table_title: str):
    if not added_models:
        return
    table = rich.table.Table(title=table_title)
    table.add_column("Model Name", style="cyan")
    table.add_column("Upstream Model", style="green")
    table.add_column("Access Groups", style="magenta")
    for m in added_models:
        table.add_row(m.model_name, m.model_id, m.access_groups_str)
    rich.print(table)

