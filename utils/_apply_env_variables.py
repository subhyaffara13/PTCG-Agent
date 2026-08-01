
def _apply_env_variables(env: dict[str, str] | None = None) -> None:
    env_dict = env if env is not None else os.environ

    for var_name, setter in [
        ("PILLOW_ALIGNMENT", core.set_alignment),
        ("PILLOW_BLOCK_SIZE", core.set_block_size),
        ("PILLOW_BLOCKS_MAX", core.set_blocks_max),
    ]:
        if var_name not in env_dict:
            continue

        var = env_dict[var_name].lower()

        units = 1
        for postfix, mul in [("k", 1024), ("m", 1024 * 1024)]:
            if var.endswith(postfix):
                units = mul
                var = var[: -len(postfix)]

        try:
            var_int = int(var) * units
        except ValueError:
            warnings.warn(f"{var_name} is not int")
            continue

        try:
            setter(var_int)
        except ValueError as e:
            warnings.warn(f"{var_name}: {e}")

