
def import_models(
    ctx: click.Context,
    yaml_file: str,
    dry_run: bool,
    only_models_matching_regex: Optional[str],
    only_access_groups_matching_regex: Optional[str],
) -> None:
    """Import models from a YAML file and add them to the proxy."""
    provider_counts: dict[str, int] = defaultdict(int)
    added_models: list[ModelYamlInfo] = []
    model_list = get_model_list_from_yaml_file(yaml_file)
    filtered_model_list = _get_filtered_model_list(
        model_list, only_models_matching_regex, only_access_groups_matching_regex
    )

    if not dry_run:
        client = create_client(ctx)

    for model in filtered_model_list:
        model_info_obj = _get_model_info_obj_from_yaml(model)
        if not dry_run:
            try:
                client.models.new(
                    model_name=model_info_obj.model_name,
                    model_params=model_info_obj.model_params,
                    model_info=model_info_obj.model_info,
                )
            except Exception:
                pass  # For summary, ignore errors
        added_models.append(model_info_obj)
        provider_counts[model_info_obj.provider] += 1

    table_title = _import_models_get_table_title(dry_run)
    _print_models_table(added_models, table_title)
    _print_summary_table(provider_counts)

