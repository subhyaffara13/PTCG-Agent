
def _decide_constant_folding(do_constant_folding, operator_export_type, training):
    do_constant_folding = _resolve_args_by_export_type(
        "do_constant_folding", do_constant_folding, operator_export_type
    )
    if do_constant_folding and (
        training is not None and training is not _C_onnx.TrainingMode.EVAL
    ):
        warnings.warn(
            "It is recommended that constant folding be turned off ('do_constant_folding=False') "
            "when exporting the model in training-amenable mode, i.e. with 'training=TrainingMode.TRAIN' "
            "or 'training=TrainingMode.PRESERVE' (when model is in training mode). Otherwise, some "
            "learnable model parameters may not translate correctly in the exported ONNX model "
            "because constant folding mutates model parameters. Please consider "
            "turning off constant folding or setting the training=TrainingMode.EVAL.",
            stacklevel=2,
        )
    return do_constant_folding

