
def test_mask_decoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    multimask_output: bool,
    dynamic_multimask_via_stability: bool,
):
    sam2_prompt_encoder = SAM2PromptEncoder(sam2_model).cpu()

    image = random_sam2_input_image()
    sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
    image_features_0, image_features_1, image_embeddings = sam2_encoder(image)

    num_labels = 1
    num_points = 5
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.float)
    input_masks = torch.rand(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.ones(1, dtype=torch.float)

    sparse_embeddings, dense_embeddings, image_pe = sam2_prompt_encoder(
        point_coords, point_labels, input_masks, has_input_masks
    )

    sam2_mask_decoder = SAM2MaskDecoder(sam2_model, multimask_output, dynamic_multimask_via_stability)
    inputs = (image_features_0, image_features_1, image_embeddings, image_pe, sparse_embeddings, dense_embeddings)
    low_res_masks, iou_predictions = sam2_mask_decoder(*inputs)

    import onnxruntime  # noqa: PLC0415

    ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    model_inputs = ort_session.get_inputs()
    input_names = [model_inputs[i].name for i in range(len(model_inputs))]
    logger.info("input_names: %s", input_names)

    model_outputs = ort_session.get_outputs()
    output_names = [model_outputs[i].name for i in range(len(model_outputs))]
    logger.info("output_names: %s", output_names)

    outputs = ort_session.run(
        output_names,
        {
            "image_features_0": image_features_0.numpy(),
            "image_features_1": image_features_1.numpy(),
            "image_embeddings": image_embeddings.numpy(),
            "image_pe": image_pe.numpy(),
            "sparse_embeddings": sparse_embeddings.numpy(),
            "dense_embeddings": dense_embeddings.numpy(),
        },
    )

    for i, output_name in enumerate(output_names):
        logger.info("output %s shape: %s", output_name, outputs[i].shape)

    ort_low_res_masks, ort_iou_predictions = outputs
    torch.testing.assert_close(low_res_masks, torch.tensor(ort_low_res_masks), atol=5e-3, rtol=1e-4)
    torch.testing.assert_close(iou_predictions, torch.tensor(ort_iou_predictions), atol=5e-3, rtol=1e-4)
    print(f"onnx model has been verified: {onnx_model_path}")

