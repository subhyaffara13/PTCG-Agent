import pathlib

def _create_config_file_path(
    model_path_or_dir: pathlib.Path,
    output_dir: pathlib.Path | None,
    optimization_level_str: str,
    optimization_style: OptimizationStyle,
    enable_type_reduction: bool,
):
    config_name = "{}{}".format(
        "required_operators_and_types" if enable_type_reduction else "required_operators",
        _optimization_suffix(optimization_level_str, optimization_style, ".config"),
    )

    if model_path_or_dir.is_dir():
        return (output_dir or model_path_or_dir) / config_name

    model_config_path = model_path_or_dir.with_suffix(f".{config_name}")

    if output_dir is not None:
        return output_dir / model_config_path.name

    return model_config_path

