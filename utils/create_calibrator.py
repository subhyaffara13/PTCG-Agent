from pathlib import Path


def create_calibrator(
    model: str | Path,
    op_types_to_calibrate: Sequence[str] | None = None,
    augmented_model_path="augmented_model.onnx",
    calibrate_method=CalibrationMethod.MinMax,
    use_external_data_format=False,
    providers=None,
    extra_options={},  # noqa: B006
):
    calibrator = None
    if calibrate_method == CalibrationMethod.MinMax:
        # default settings for min-max algorithm
        symmetric = extra_options.get("symmetric", False)
        moving_average = extra_options.get("moving_average", False)
        averaging_constant = extra_options.get("averaging_constant", 0.01)
        max_intermediate_outputs = extra_options.get("max_intermediate_outputs", None)
        per_channel = extra_options.get("per_channel", False)
        calibrator = MinMaxCalibrater(
            model,
            op_types_to_calibrate,
            augmented_model_path,
            use_external_data_format=use_external_data_format,
            symmetric=symmetric,
            moving_average=moving_average,
            averaging_constant=averaging_constant,
            max_intermediate_outputs=max_intermediate_outputs,
            per_channel=per_channel,
        )
    elif calibrate_method == CalibrationMethod.Entropy:
        # default settings for entropy algorithm
        num_bins = extra_options.get("num_bins", 128)
        num_quantized_bins = extra_options.get("num_quantized_bins", 128)
        symmetric = extra_options.get("symmetric", False)
        calibrator = EntropyCalibrater(
            model,
            op_types_to_calibrate,
            augmented_model_path,
            use_external_data_format=use_external_data_format,
            symmetric=symmetric,
            num_bins=num_bins,
            num_quantized_bins=num_quantized_bins,
        )
    elif calibrate_method == CalibrationMethod.Percentile:
        # default settings for percentile algorithm
        num_bins = extra_options.get("num_bins", 2048)
        percentile = extra_options.get("percentile", 99.999)
        symmetric = extra_options.get("symmetric", True)
        calibrator = PercentileCalibrater(
            model,
            op_types_to_calibrate,
            augmented_model_path,
            use_external_data_format=use_external_data_format,
            symmetric=symmetric,
            num_bins=num_bins,
            percentile=percentile,
        )

    elif calibrate_method == CalibrationMethod.Distribution:
        # default settings for percentile algorithm
        num_bins = extra_options.get("num_bins", 2048)
        scenario = extra_options.get("scenario", "same")

        calibrator = DistributionCalibrater(
            model,
            op_types_to_calibrate,
            augmented_model_path,
            use_external_data_format=use_external_data_format,
            num_bins=num_bins,
            scenario=scenario,
        )

    if calibrator:
        calibrator.augment_graph()
        if providers:
            calibrator.execution_providers = providers
        calibrator.create_inference_session()
        return calibrator

    raise ValueError(f"Unsupported calibration method {calibrate_method}")

