
def export_decoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    multimask_output: bool = False,
    verbose: bool = False,
):
    batch_size = 1
    image = random_sam2_input_image(batch_size)
    sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
    image_features_0, image_features_1, image_embeddings = sam2_encoder(image)

    logger.info("image_features_0.shape: %s", image_features_0.shape)
    logger.info("image_features_1.shape: %s", image_features_1.shape)
    logger.info("image_embeddings.shape: %s", image_embeddings.shape)

    sam2_decoder = SAM2ImageDecoder(
        sam2_model,
        multimask_output=multimask_output,
        dynamic_multimask_via_stability=True,
    ).cpu()

    num_labels = 2
    num_points = 3
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.int32)
    input_masks = torch.zeros(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.ones(1, dtype=torch.float)
    original_image_size = torch.tensor([1200, 1800], dtype=torch.int32)

    example_inputs = (
        image_features_0,
        image_features_1,
        image_embeddings,
        point_coords,
        point_labels,
        input_masks,
        has_input_masks,
        original_image_size,
    )

    logger.info("point_coords.shape: %s", point_coords.shape)
    logger.info("point_labels.shape: %s", point_labels.shape)
    logger.info("input_masks.shape: %s", input_masks.shape)
    logger.info("has_input_masks.shape: %s", has_input_masks.shape)
    logger.info("original_image_size.shape: %s", original_image_size.shape)

    if verbose:
        masks, iou_predictions, low_res_masks = sam2_decoder(*example_inputs)
        logger.info("masks.shape: %s", masks.shape)
        logger.info("iou_predictions.shape: %s", iou_predictions.shape)
        logger.info("low_res_masks.shape: %s", low_res_masks.shape)

    input_names = [
        "image_features_0",
        "image_features_1",
        "image_embeddings",
        "point_coords",
        "point_labels",
        "input_masks",
        "has_input_masks",
        "original_image_size",
    ]

    output_names = ["masks", "iou_predictions", "low_res_masks"]

    dynamic_axes = {
        "point_coords": {0: "num_labels", 1: "num_points"},
        "point_labels": {0: "num_labels", 1: "num_points"},
        "input_masks": {0: "num_labels"},
        "has_input_masks": {0: "num_labels"},
        "masks": {0: "num_labels", 2: "original_image_height", 3: "original_image_width"},
        "low_res_masks": {0: "num_labels"},
        "iou_predictions": {0: "num_labels"},
    }

    with warnings.catch_warnings():
        if not verbose:
            warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
            warnings.filterwarnings("ignore", category=UserWarning)

        torch.onnx.export(
            sam2_decoder,
            example_inputs,
            onnx_model_path,
            export_params=True,
            opset_version=16,
            do_constant_folding=True,
            input_names=input_names,
            output_names=output_names,
            dynamic_axes=dynamic_axes,
        )

    logger.info("decoder onnx model saved to %s", onnx_model_path)

