
def exporter_context(model, mode: _C_onnx.TrainingMode, verbose: bool):
    """A context manager to temporarily set the training mode of ``model``
    to ``mode``, disable the Apex O2 hook, and set the ONNX logging verbosity.

    .. deprecated:: 2.7
        Please set training mode before exporting the model.
    """
    with (
        select_model_mode_for_export(model, mode) as mode_ctx,
        disable_apex_o2_state_dict_hook(model) as apex_ctx,
        setup_onnx_logging(verbose) as log_ctx,
    ):
        yield (mode_ctx, apex_ctx, log_ctx)

