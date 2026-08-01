
def export_prompt_encoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
):
    sam2_prompt_encoder = SAM2PromptEncoder(sam2_model).cpu()

    num_labels = 2
    num_points = 3
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.int32)
    input_masks = torch.zeros(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.ones(1, dtype=torch.float)

    sparse_embeddings, dense_embeddings, image_pe = sam2_prompt_encoder(
        point_coords, point_labels, input_masks, has_input_masks
    )

    logger.info("point_coords.shape: %s", point_coords.shape)
    logger.info("point_labels.shape: %s", point_labels.shape)
    logger.info("input_masks.shape: %s", input_masks.shape)
    logger.info("has_input_masks.shape: %s", has_input_masks.shape)

    logger.info("sparse_embeddings.shape: %s", sparse_embeddings.shape)
    logger.info("dense_embeddings.shape: %s", dense_embeddings.shape)
    logger.info("image_pe.shape: %s", image_pe.shape)

    torch.onnx.export(
        sam2_prompt_encoder,
        (point_coords, point_labels, input_masks, has_input_masks),
        onnx_model_path,
        export_params=True,
        opset_version=18,
        do_constant_folding=True,
        input_names=["point_coords", "point_labels", "input_masks", "has_input_masks"],
        output_names=["sparse_embeddings", "dense_embeddings", "image_pe"],
        dynamic_axes={
            "point_coords": {0: "num_labels", 1: "num_points"},
            "point_labels": {0: "num_labels", 1: "num_points"},
            "input_masks": {0: "num_labels"},
            "sparse_embeddings": {0: "num_labels", 1: "num_points+1"},
            "dense_embeddings": {0: "num_labels"},
        },
    )

    print("prompt encoder onnx model saved to ", onnx_model_path)

