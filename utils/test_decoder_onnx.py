
def test_decoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    multimask_output=False,
):
    batch_size = 1
    image = random_sam2_input_image(batch_size)
    sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
    image_features_0, image_features_1, image_embeddings = sam2_encoder(image)

    sam2_image_decoder = SAM2ImageDecoder(
        sam2_model,
        multimask_output=multimask_output,
        dynamic_multimask_via_stability=True,
    ).cpu()

    num_labels = 1
    num_points = 5
    point_coords = torch.randint(low=0, high=1024, size=(num_labels, num_points, 2), dtype=torch.float)
    point_labels = torch.randint(low=0, high=1, size=(num_labels, num_points), dtype=torch.int32)
    input_masks = torch.zeros(num_labels, 1, 256, 256, dtype=torch.float)
    has_input_masks = torch.zeros(1, dtype=torch.float)
    original_image_size = torch.tensor([1500, 1500], dtype=torch.int32)

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

    masks, iou_predictions, low_res_masks = sam2_image_decoder(*example_inputs)

    import onnxruntime  # noqa: PLC0415

    ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    model_inputs = ort_session.get_inputs()
    input_names = [model_inputs[i].name for i in range(len(model_inputs))]
    logger.info("input_names: %s", input_names)

    model_outputs = ort_session.get_outputs()
    output_names = [model_outputs[i].name for i in range(len(model_outputs))]
    logger.info("output_names: %s", output_names)
    inputs = {model_inputs[i].name: example_inputs[i].numpy() for i in range(len(model_inputs))}
    outputs = ort_session.run(output_names, inputs)

    for i, output_name in enumerate(output_names):
        logger.info(f"{output_name}.shape: %s", outputs[i].shape)

    ort_masks, ort_iou_predictions, ort_low_res_masks = outputs
    if (
        compare_tensors_with_tolerance("masks", masks.float(), torch.tensor(ort_masks).float())
        and compare_tensors_with_tolerance("iou_predictions", iou_predictions, torch.tensor(ort_iou_predictions))
        and compare_tensors_with_tolerance("low_res_masks", low_res_masks, torch.tensor(ort_low_res_masks))
    ):
        print("onnx model has been verified:", onnx_model_path)
    else:
        print("onnx model verification failed:", onnx_model_path)

