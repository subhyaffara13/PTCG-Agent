
def export_mask_decoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    multimask_output: bool,
    dynamic_multimask_via_stability: bool = True,
    verbose=False,
):
    sam2_prompt_encoder = SAM2PromptEncoder(sam2_model).cpu()

    image = random_sam2_input_image()
    sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
    image_features_0, image_features_1, image_embeddings = sam2_encoder(image)
    logger.info("image_features_0.shape: %s", image_features_0.shape)
    logger.info("image_features_1.shape: %s", image_features_1.shape)
    logger.info("image_embeddings.shape: %s", image_embeddings.shape)

    # encode an random prompt
    num_labels = 2
    num_points = 3
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.float)
    input_masks = torch.zeros(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.ones(1, dtype=torch.float)

    sparse_embeddings, dense_embeddings, image_pe = sam2_prompt_encoder(
        point_coords, point_labels, input_masks, has_input_masks
    )

    logger.info("sparse_embeddings.shape: %s", sparse_embeddings.shape)
    logger.info("dense_embeddings.shape: %s", dense_embeddings.shape)
    logger.info("image_pe.shape: %s", image_pe.shape)

    sam2_mask_decoder = SAM2MaskDecoder(sam2_model, multimask_output, dynamic_multimask_via_stability)
    inputs = (image_features_0, image_features_1, image_embeddings, image_pe, sparse_embeddings, dense_embeddings)
    low_res_masks, iou_predictions = sam2_mask_decoder(*inputs)
    logger.info("low_res_masks.shape: %s", low_res_masks.shape)
    logger.info("iou_predictions.shape: %s", iou_predictions.shape)

    with warnings.catch_warnings():
        if not verbose:
            warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
            warnings.filterwarnings("ignore", category=UserWarning)
        torch.onnx.export(
            sam2_mask_decoder,
            inputs,
            onnx_model_path,
            export_params=True,
            opset_version=18,
            do_constant_folding=True,
            input_names=[
                "image_features_0",
                "image_features_1",
                "image_embeddings",
                "image_pe",
                "sparse_embeddings",
                "dense_embeddings",
            ],
            output_names=["low_res_masks", "iou_predictions"],
            dynamic_axes={
                "sparse_embeddings": {0: "num_labels", 1: "num_points+1"},
                "dense_embeddings": {0: "num_labels"},
                "low_res_masks": {0: "num_labels"},
                "iou_predictions": {0: "num_labels"},
            },
        )

    print("mask decoder onnx model saved to", onnx_model_path)

