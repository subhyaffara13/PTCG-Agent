
def test_prompt_encoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
):
    sam2_prompt_encoder = SAM2PromptEncoder(sam2_model).cpu()

    num_labels = 1
    num_points = 5
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.int32)
    input_masks = torch.rand(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.ones(1, dtype=torch.float)

    sparse_embeddings, dense_embeddings, image_pe = sam2_prompt_encoder(
        point_coords, point_labels, input_masks, has_input_masks
    )

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
            "point_coords": point_coords.numpy(),
            "point_labels": point_labels.numpy(),
            "input_masks": input_masks.numpy(),
            "has_input_masks": has_input_masks.numpy(),
        },
    )

    for i, output_name in enumerate(output_names):
        logger.info("output %s shape: %s", output_name, outputs[i].shape)

    ort_sparse_embeddings, ort_dense_embeddings, ort_image_pe = outputs
    if (
        compare_tensors_with_tolerance(
            "sparse_embeddings",
            sparse_embeddings,
            torch.tensor(ort_sparse_embeddings),
            mismatch_percentage_tolerance=0.2,
        )
        and compare_tensors_with_tolerance(
            "dense_embeddings", dense_embeddings, torch.tensor(ort_dense_embeddings), mismatch_percentage_tolerance=0.2
        )
        and compare_tensors_with_tolerance(
            "image_pe", image_pe, torch.tensor(ort_image_pe), mismatch_percentage_tolerance=0.2
        )
    ):
        print(f"onnx model has been verified: {onnx_model_path}")
    else:
        print(f"onnx model verification failed: {onnx_model_path}")

