
def unregister_custom_op_symbolic(symbolic_name: str, opset_version: int) -> None:
    """Unregisters ``symbolic_name``.

    See "Custom Operators" in the module documentation for an example usage.

    Args:
        symbolic_name (str): The name of the custom operator in "<domain>::<op>"
            format.
        opset_version (int): The ONNX opset version in which to unregister.
    """
    if symbolic_name.startswith("::"):
        symbolic_name = f"aten{symbolic_name}"

    _verify_custom_op_name(symbolic_name)

    registration.registry.unregister(symbolic_name, opset_version)

