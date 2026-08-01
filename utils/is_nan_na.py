
def is_nan_na() -> bool:
    _mode_options = _global_config["future"]
    return not _mode_options["distinguish_nan_and_na"]

