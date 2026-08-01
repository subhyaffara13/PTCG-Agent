
def test_image_encoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    dynamic_batch_axes=False,
):
    ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

    model_inputs = ort_session.get_inputs()
    input_names = [model_inputs[i].name for i in range(len(model_inputs))]
    logger.info("input_names: %s", input_names)

    model_outputs = ort_session.get_outputs()
    output_names = [model_outputs[i].name for i in range(len(model_outputs))]
    logger.info("output_names: %s", output_names)

    batch_sizes = [1, 2] if dynamic_batch_axes else [1]
    for batch_size in batch_sizes:
        image = random_sam2_input_image(batch_size)

        sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
        image_features_0, image_features_1, image_embeddings = sam2_encoder(image.clone())

        logger.info("image.shape: %s", image.shape)
        logger.info("image_features_0.shape: %s", image_features_0.shape)
        logger.info("image_features_1.shape: %s", image_features_1.shape)
        logger.info("image_embeddings.shape: %s", image_embeddings.shape)

        outputs = ort_session.run(output_names, {"image": image.numpy()})
        for i, output_name in enumerate(output_names):
            logger.info("output %s shape %s", output_name, outputs[i].shape)
        ort_image_features_0, ort_image_features_1, ort_image_embeddings = outputs

        # ONNXRuntime and PyTorch has about 0.75% mismatched elements, but seems not impacting segmentation results.
        if (
            compare_tensors_with_tolerance(
                "image_features_0",
                image_features_0,
                torch.tensor(ort_image_features_0),
                mismatch_percentage_tolerance=1,
            )
            and compare_tensors_with_tolerance(
                "image_features_1",
                image_features_1,
                torch.tensor(ort_image_features_1),
                mismatch_percentage_tolerance=1,
            )
            and compare_tensors_with_tolerance(
                "image_embeddings",
                image_embeddings,
                torch.tensor(ort_image_embeddings),
                mismatch_percentage_tolerance=1,
            )
        ):
            print(f"onnx model has been verified for batch_size={batch_size}: {onnx_model_path}")
        else:
            print(f"onnx model verification failed for batch_size={batch_size}: {onnx_model_path}")

