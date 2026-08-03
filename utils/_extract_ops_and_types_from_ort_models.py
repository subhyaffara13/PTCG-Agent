import pathlib

def _extract_ops_and_types_from_ort_models(model_files: typing.Iterable[pathlib.Path], enable_type_reduction: bool):
    required_ops = {}
    op_type_usage_manager = OperatorTypeUsageManager() if enable_type_reduction else None

    for model_file in model_files:
        if not model_file.is_file():
            raise ValueError(f"Path is not a file: '{model_file}'")
        model_processor = OrtFormatModelProcessor(str(model_file), required_ops, op_type_usage_manager)
        model_processor.process()  # this updates required_ops and op_type_processors

    return required_ops, op_type_usage_manager

