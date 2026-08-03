import os
import pathlib

def convert_onnx_models_to_ort(
    model_path_or_dir: pathlib.Path,
    output_dir: pathlib.Path | None = None,
    optimization_styles: list[OptimizationStyle] | None = None,
    custom_op_library_path: pathlib.Path | None = None,
    target_platform: str | None = None,
    save_optimized_onnx_model: bool = False,
    allow_conversion_failures: bool = False,
    enable_type_reduction: bool = False,
):
    if output_dir is not None:
        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)
        output_dir = output_dir.resolve(strict=True)

    optimization_styles = optimization_styles or []

    # setting optimization level is not expected to be needed by typical users, but it can be set with this
    # environment variable
    optimization_level_str = os.getenv("ORT_CONVERT_ONNX_MODELS_TO_ORT_OPTIMIZATION_LEVEL", "all")
    model_path_or_dir = model_path_or_dir.resolve()
    custom_op_library = custom_op_library_path.resolve() if custom_op_library_path else None

    if not model_path_or_dir.is_dir() and not model_path_or_dir.is_file():
        raise FileNotFoundError(f"Model path '{model_path_or_dir}' is not a file or directory.")

    if custom_op_library and not custom_op_library.is_file():
        raise FileNotFoundError(f"Unable to find custom operator library '{custom_op_library}'")

    session_options_config_entries = {}

    if target_platform is not None and target_platform == "arm":
        session_options_config_entries["session.qdqisint8allowed"] = "1"
    else:
        session_options_config_entries["session.qdqisint8allowed"] = "0"

    for optimization_style in optimization_styles:
        print(
            f"Converting models with optimization style '{optimization_style.name}' and level '{optimization_level_str}'"
        )

        converted_models = _convert(
            model_path_or_dir=model_path_or_dir,
            output_dir=output_dir,
            optimization_level_str=optimization_level_str,
            optimization_style=optimization_style,
            custom_op_library=custom_op_library,
            create_optimized_onnx_model=save_optimized_onnx_model,
            allow_conversion_failures=allow_conversion_failures,
            target_platform=target_platform,
            session_options_config_entries=session_options_config_entries,
        )

        with contextlib.ExitStack() as context_stack:
            if optimization_style == OptimizationStyle.Runtime:
                # Convert models again without runtime optimizations.
                # Runtime optimizations may not end up being applied, so we need to use both converted models with and
                # without runtime optimizations to get a complete set of ops that may be needed for the config file.
                model_dir = model_path_or_dir if model_path_or_dir.is_dir() else model_path_or_dir.parent
                temp_output_dir = context_stack.enter_context(
                    tempfile.TemporaryDirectory(dir=model_dir, suffix=".without_runtime_opt")
                )
                session_options_config_entries_for_second_conversion = session_options_config_entries.copy()
                # Limit the optimizations to those that can run in a model with runtime optimizations.
                session_options_config_entries_for_second_conversion["optimization.minimal_build_optimizations"] = (
                    "apply"
                )

                print(
                    "Converting models again without runtime optimizations to generate a complete config file. "
                    "These converted models are temporary and will be deleted."
                )
                converted_models += _convert(
                    model_path_or_dir=model_path_or_dir,
                    output_dir=temp_output_dir,
                    optimization_level_str=optimization_level_str,
                    optimization_style=OptimizationStyle.Fixed,
                    custom_op_library=custom_op_library,
                    create_optimized_onnx_model=False,  # not useful as they would be created in a temp directory
                    allow_conversion_failures=allow_conversion_failures,
                    target_platform=target_platform,
                    session_options_config_entries=session_options_config_entries_for_second_conversion,
                )

            print(
                f"Generating config file from ORT format models with optimization style '{optimization_style.name}' and level '{optimization_level_str}'"
            )

            config_file = _create_config_file_path(
                model_path_or_dir,
                output_dir,
                optimization_level_str,
                optimization_style,
                enable_type_reduction,
            )

            create_config_from_models(converted_models, config_file, enable_type_reduction)

