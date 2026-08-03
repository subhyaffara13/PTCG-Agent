from typing import Any

def parse_native_functions_keys(
    backend_yaml_path: str,
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
) -> tuple[list[OperatorName], list[Any], list[OperatorName]]:
    with open(backend_yaml_path) as f:
        yaml_values = yaml.load(f, Loader=YamlLoader)
    if not isinstance(yaml_values, dict):
        raise AssertionError(f"Expected dict from YAML, got {type(yaml_values)}")

    full_codegen = yaml_values.pop("full_codegen", [])
    non_native = yaml_values.pop("non_native", [])
    ir_gen = yaml_values.pop("ir_gen", [])
    if not isinstance(full_codegen, list):
        raise AssertionError(
            f"Expected full_codegen to be list, got {type(full_codegen)}"
        )
    if not isinstance(non_native, list):
        raise AssertionError(f"Expected non_native to be list, got {type(non_native)}")
    if not isinstance(ir_gen, list):
        raise AssertionError(f"Expected ir_gen to be list, got {type(ir_gen)}")
    full_codegen_opnames = [OperatorName.parse(name) for name in full_codegen]
    ir_gen_opnames = [OperatorName.parse(name) for name in ir_gen]
    return full_codegen_opnames, non_native, ir_gen_opnames

