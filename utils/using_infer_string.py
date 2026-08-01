
def using_infer_string() -> bool:
    """
    Fixture to check if infer string option is enabled.
    """
    return pd.options.future.infer_string is True

