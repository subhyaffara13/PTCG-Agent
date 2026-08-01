
def _get_tensor_info_op_configs(dtype_configs):
    """
    These ops work on tensors of different dtypes but return non-tensors
    containing information about the input tensor.
    """

    def _get_config(op):
        return (
            BackendPatternConfig(op)
            .set_observation_type(ObservationType.INPUT_OUTPUT_NOT_OBSERVED)
            .set_dtype_configs(dtype_configs)
        )

    return [_get_config(op) for op in ("shape", "size")]

