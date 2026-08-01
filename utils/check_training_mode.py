
def check_training_mode(op_train_mode: int, op_name: str) -> None:
    """Warns the user if the model's training mode and the export mode do not agree."""
    if GLOBALS.training_mode == _C_onnx.TrainingMode.PRESERVE:
        return

    if op_train_mode:
        op_mode_enum = _C_onnx.TrainingMode.TRAINING
    else:
        op_mode_enum = _C_onnx.TrainingMode.EVAL
    if op_mode_enum == GLOBALS.training_mode:
        # The modes agree. Do nothing
        return

    op_mode_text = f"train={bool(op_train_mode)}"
    # Setting the model mode could result in op_mode != GLOBALS.training_mode
    # if the model is a FuncModule. In this case we warn the user of
    # the state and export depending on op_mode
    # This is to support use-cases of fixing certain layer weights
    # in training.
    warnings.warn(
        f"ONNX export mode is set to {GLOBALS.training_mode}, but operator '{op_name}' "
        f"is set to {op_mode_text}. Exporting with {op_mode_text}.",
        stacklevel=2,
    )

