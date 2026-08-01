
def _create_session_options(
    optimization_level: ort.GraphOptimizationLevel,
    output_model_path: pathlib.Path,
    custom_op_library: pathlib.Path,
    session_options_config_entries: dict[str, str],
):
    so = ort.SessionOptions()
    so.optimized_model_filepath = str(output_model_path)
    so.graph_optimization_level = optimization_level

    if custom_op_library:
        so.register_custom_ops_library(str(custom_op_library))

    for key, value in session_options_config_entries.items():
        so.add_session_config_entry(key, value)

    return so

