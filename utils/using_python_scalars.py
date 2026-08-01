
def using_python_scalars() -> bool:
    return pd.options.future.python_scalars is True


def using_python_scalars() -> bool:
    _mode_options = _global_config["future"]
    return _mode_options["python_scalars"]

