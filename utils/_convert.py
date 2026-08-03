import copy
import pathlib
import re

def _convert(camel_input):
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", camel_input)
    return "_".join(map(str.lower, words))


def _convert(ret, cls):
    if cls is Tensor:
        return ret

    if isinstance(ret, Tensor) and not isinstance(ret, cls):
        ret = ret.as_subclass(cls)

    if isinstance(ret, (tuple, list)):
        # Also handles things like namedtuples
        ret = type(ret)(_convert(r, cls) for r in ret)

    return ret


def _convert(
    module,
    mapping=None,
    inplace=False,
    is_reference=False,
    convert_custom_config_dict=None,
    use_precomputed_fake_quant=False,
):
    r"""Converts submodules in input module to a different module according to `mapping`
    by calling `from_float` method on the target module class

    Args:
        module: input module
        mapping: a dictionary that maps from source module type to target
                 module type, can be overwritten to allow swapping user defined
                 Modules
        inplace: carry out model transformations in-place, the original module
                 is mutated
        is_reference: a flag to enable quantized reference module
        use_precomputed_fake_quant: a flag to enable use of precomputed fake quant

    """
    if mapping is None:
        mapping = (
            get_default_static_quant_reference_module_mappings()
            if is_reference
            else get_default_static_quant_module_mappings()
        )
    if convert_custom_config_dict is None:
        convert_custom_config_dict = get_default_custom_config_dict()
    custom_module_class_mapping = convert_custom_config_dict.get(
        "observed_to_quantized_custom_module_class", {}
    )

    if not inplace:
        module = copy.deepcopy(module)
    reassign = {}
    for name, mod in module.named_children():
        # both fused modules and observed custom modules are
        # swapped as one unit
        if (
            not isinstance(mod, _FusedModule)
            and type_before_parametrizations(mod) not in custom_module_class_mapping
        ):
            _convert(
                mod,
                mapping,
                True,  # inplace
                is_reference,
                convert_custom_config_dict,
                use_precomputed_fake_quant=use_precomputed_fake_quant,
            )
        reassign[name] = swap_module(
            mod, mapping, custom_module_class_mapping, use_precomputed_fake_quant
        )

    for key, value in reassign.items():
        module._modules[key] = value

    return module


def _convert(
    model_path_or_dir: pathlib.Path,
    output_dir: pathlib.Path | None,
    optimization_level_str: str,
    optimization_style: OptimizationStyle,
    custom_op_library: pathlib.Path,
    create_optimized_onnx_model: bool,
    allow_conversion_failures: bool,
    target_platform: str,
    session_options_config_entries: dict[str, str],
) -> list[pathlib.Path]:
    model_dir = model_path_or_dir if model_path_or_dir.is_dir() else model_path_or_dir.parent
    output_dir = output_dir or model_dir

    optimization_level = get_optimization_level(optimization_level_str)

    def is_model_file_to_convert(file_path: pathlib.Path):
        if not path_match_suffix_ignore_case(file_path, ".onnx"):
            return False
        # ignore any files with an extension of .optimized.onnx which are presumably from previous executions
        # of this script
        if path_match_suffix_ignore_case(file_path, ".optimized.onnx"):
            print(f"Ignoring '{file_path}'")
            return False
        return True

    models = files_from_file_or_dir(model_path_or_dir, is_model_file_to_convert)

    if len(models) == 0:
        raise ValueError(f"No model files were found in '{model_path_or_dir}'")

    providers = ["CPUExecutionProvider"]

    # if the optimization level is greater than or equal to 'layout' we manually exclude the NCHWc transformer.
    # It's not applicable to ARM devices, and creates a device specific model which won't run on all hardware.
    # If someone really really really wants to run it they could manually create an optimized onnx model first,
    # or they could comment out this code.
    optimizer_filter = None
    if (
        (optimization_level == ort.GraphOptimizationLevel.ORT_ENABLE_ALL)
        or (optimization_level == ort.GraphOptimizationLevel.ORT_ENABLE_LAYOUT)
    ) and target_platform != "amd64":
        optimizer_filter = ["NchwcTransformer"]

    converted_models = []

    for model in models:
        try:
            relative_model_path = model.relative_to(model_dir)

            (output_dir / relative_model_path).parent.mkdir(parents=True, exist_ok=True)

            ort_target_path = (output_dir / relative_model_path).with_suffix(
                _optimization_suffix(optimization_level_str, optimization_style, ".ort")
            )

            if create_optimized_onnx_model:
                # Create an ONNX file with the same optimization level that will be used for the ORT format file.
                # This allows the ONNX equivalent of the ORT format model to be easily viewed in Netron.
                # If runtime optimizations are saved in the ORT format model, there may be some difference in the
                # graphs at runtime between the ORT format model and this saved ONNX model.
                optimized_target_path = (output_dir / relative_model_path).with_suffix(
                    _optimization_suffix(optimization_level_str, optimization_style, ".optimized.onnx")
                )
                so = _create_session_options(
                    optimization_level, optimized_target_path, custom_op_library, session_options_config_entries
                )
                if optimization_style == OptimizationStyle.Runtime:
                    # Limit the optimizations to those that can run in a model with runtime optimizations.
                    so.add_session_config_entry("optimization.minimal_build_optimizations", "apply")

                print(f"Saving optimized ONNX model {model} to {optimized_target_path}")
                _ = ort.InferenceSession(
                    str(model), sess_options=so, providers=providers, disabled_optimizers=optimizer_filter
                )

            # Load ONNX model, optimize, and save to ORT format
            so = _create_session_options(
                optimization_level, ort_target_path, custom_op_library, session_options_config_entries
            )
            so.add_session_config_entry("session.save_model_format", "ORT")
            if optimization_style == OptimizationStyle.Runtime:
                so.add_session_config_entry("optimization.minimal_build_optimizations", "save")

            print(f"Converting optimized ONNX model {model} to ORT format model {ort_target_path}")
            _ = ort.InferenceSession(
                str(model), sess_options=so, providers=providers, disabled_optimizers=optimizer_filter
            )

            converted_models.append(ort_target_path)

            # orig_size = os.path.getsize(onnx_target_path)
            # new_size = os.path.getsize(ort_target_path)
            # print("Serialized {} to {}. Sizes: orig={} new={} diff={} new:old={:.4f}:1.0".format(
            #     onnx_target_path, ort_target_path, orig_size, new_size, new_size - orig_size, new_size / orig_size))
        except Exception as e:
            print(f"Error converting {model}: {e}")
            if not allow_conversion_failures:
                raise

    print(f"Converted {len(converted_models)}/{len(models)} models successfully.")

    return converted_models

