
def describe_input(i: int, aot_config: AOTConfig) -> str:
    if i < aot_config.num_params_buffers:
        return f"parameter/buffer {i}"
    else:
        return f"input {i - aot_config.num_params_buffers}"

