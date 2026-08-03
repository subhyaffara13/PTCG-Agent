import logging
import pathlib

def update_onnx_opset(
    model_path: pathlib.Path,
    opset: int,
    out_path: pathlib.Path | None = None,
    logger: logging.Logger | None = None,
):
    """
    Helper to update the opset of a model using onnx version_converter. Target opset must be greater than current opset.
    :param model_path: Path to model to update
    :param opset: Opset to update model to
    :param out_path: Optional output path for updated model to be saved to.
    :param logger: Optional logger for diagnostic output
    :returns: Updated onnx.ModelProto
    """

    model_path_str = str(model_path.resolve(strict=True))
    if logger:
        logger.info("Updating %s to opset %d", model_path_str, opset)

    model = onnx.load(model_path_str)

    new_model = version_converter.convert_version(model, opset)

    if out_path:
        onnx.save(new_model, str(out_path))
        if logger:
            logger.info("Saved updated model to %s", out_path)

    return new_model

