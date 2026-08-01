
def serialize_model(
    module, inputs, *, config=None, return_shapes=None, use_int16_for_qint16=False
):
    """Convert to NNAPI and serialize torchscript module.

    Parameters:
        module: Torchscript module to convert
        inputs: Tensors used to specify input details for NNAPI
        config (optional): Optional config to attach to module
        return_shapes (optional): Specify shape of outputs if
            your module uses runtime flexible shapes to set output
            buffer size for NNAPI
        use_int16_for_qint16 (optional): Use Pytorch int16 to represent NNAPI qint16 values
    """
    return _NnapiSerializer(config, use_int16_for_qint16).serialize_model(
        module, inputs, return_shapes
    )

