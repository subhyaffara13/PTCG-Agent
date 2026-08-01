
def using_string_dtype() -> bool:
    _mode_options = _global_config["future"]
    return _mode_options["infer_string"]

