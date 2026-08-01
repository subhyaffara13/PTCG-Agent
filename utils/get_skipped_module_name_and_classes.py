
def get_skipped_module_name_and_classes(
    prepare_custom_config: PrepareCustomConfig, is_standalone_module: bool
) -> tuple[list[str], list[type[Any]]]:
    skipped_module_names = copy.copy(prepare_custom_config.non_traceable_module_names)
    skipped_module_classes = copy.copy(
        prepare_custom_config.non_traceable_module_classes
    )
    if not is_standalone_module:
        # standalone module and custom module config are applied in top level module
        skipped_module_names += list(
            prepare_custom_config.standalone_module_names.keys()
        )
        skipped_module_classes += list(
            prepare_custom_config.standalone_module_classes.keys()
        )
        skipped_module_classes += get_custom_module_class_keys(
            prepare_custom_config.float_to_observed_mapping
        )

    return skipped_module_names, skipped_module_classes

