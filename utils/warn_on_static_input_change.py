
def warn_on_static_input_change(input_states) -> None:
    """Warns that changes to input dictionaries and strings won't take effect in the traced ONNX graph.

    We accept dictionaries and strings as ONNX inputs, but they should be only for
    configuration use. we detect here if these inputs are modified, and if so we warn
    the user that the changes won't take effect in the traced ONNX graph.
    """
    for input, traced_input in zip(input_states[0], input_states[1]):
        if isinstance(input, dict):
            if list(input.keys()) != list(traced_input.keys()):
                warning = (
                    "We detected that you are modifying a dictionary that is an input to your "
                    "model. "
                    "Note that dictionaries are allowed as inputs in ONNX but they should be "
                    "handled with care. "
                    "Usages of dictionaries is not recommended, and should not be used except "
                    "for configuration use. "
                    "Also note that the order and values of the keys must remain the same. "
                )
                warnings.warn(warning, stacklevel=2)
        elif isinstance(input, str):
            if input != traced_input:
                warning = (
                    "The model seems to have string inputs/outputs. "
                    "Note that strings will not appear as inputs/outputs of the ONNX graph. "
                )
                warnings.warn(warning, stacklevel=2)

