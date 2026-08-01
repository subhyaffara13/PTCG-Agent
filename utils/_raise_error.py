
def _raise_error(method_name, _):
    raise RuntimeError(
        f"Placement method '{method_name}' should not be called as "
        "it should be overridden by the subclass"
    )

