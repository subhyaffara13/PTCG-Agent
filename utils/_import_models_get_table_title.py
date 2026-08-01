
def _import_models_get_table_title(dry_run: bool) -> str:
    if dry_run:
        return "Models that would be imported if [yellow]--dry-run[/yellow] was not provided"
    else:
        return "Models Imported"

