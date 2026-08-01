
def export_image_encoder_onnx(
    sam2_model: SAM2Base,
    onnx_model_path: str,
    dynamic_batch_axes: bool = False,
    verbose: bool = False,
    dynamo: bool = False,
    clear_dynamo_metadata: bool = False,
):
    image = random_sam2_input_image()

    sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
    image_features_0, image_features_1, image_embeddings = sam2_encoder(image)
    logger.info("image.shape: %s", image.shape)
    logger.info("image_features_0.shape: %s", image_features_0.shape)
    logger.info("image_features_1.shape: %s", image_features_1.shape)
    logger.info("image_embeddings.shape: %s", image_embeddings.shape)

    dynamic_axes = None
    if dynamic_batch_axes:
        dynamic_axes = {
            "image": {0: "batch_size"},
            "image_features_0": {0: "batch_size"},
            "image_features_1": {0: "batch_size"},
            "image_embeddings": {0: "batch_size"},
        }

    with warnings.catch_warnings():
        if not verbose:
            warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
            warnings.filterwarnings("ignore", category=UserWarning)

        if not dynamo:
            torch.onnx.export(
                sam2_encoder,
                image,
                onnx_model_path,
                export_params=True,
                opset_version=17,
                do_constant_folding=True,
                input_names=["image"],
                output_names=["image_features_0", "image_features_1", "image_embeddings"],
                dynamic_axes=dynamic_axes,
            )
        else:
            torch._dynamo.config.capture_scalar_outputs = True
            ep = torch.export.export(
                sam2_encoder,
                args=(image,),
                strict=False,
                dynamic_shapes=[
                    {0: torch.export.Dim.AUTO},
                ],
            )

            onnx_program = torch.onnx.export(
                ep,
                (),
                opset_version=17,
                input_names=["image"],
                output_names=["image_features_0", "image_features_1", "image_embeddings"],
                dynamo=True,
            )
            onnx_program.optimize()
            onnx_program.save(onnx_model_path + ".dynamo.onnx", external_data=False)
            import onnx  # noqa: PLC0415

            from onnxruntime.transformers.dynamo_onnx_helper import DynamoOnnxHelper  # noqa: PLC0415

            onnx_model = onnx.load_model(onnx_model_path + ".dynamo.onnx", load_external_data=True)
            if dynamic_batch_axes:
                # Fix labels of dynamic axes since they can't be specified during Dynamo export currently
                onnx_model.graph.input[0].type.tensor_type.shape.dim[0].dim_param = "batch_size"
                for i in range(3):
                    onnx_model.graph.output[i].type.tensor_type.shape.dim[0].dim_param = "batch_size"

            onnx_model_helper = DynamoOnnxHelper(onnx_model)
            onnx_model_helper.convert_constants_to_initializers()
            if clear_dynamo_metadata:
                onnx_model_helper.clear_metadata()

            import os  # noqa: PLC0415

            if os.path.exists(onnx_model_path):
                os.remove(onnx_model_path)
            if os.path.exists(onnx_model_path + ".data"):
                os.remove(onnx_model_path + ".data")
            onnx_model_helper.model.save_model_to_file(
                onnx_model_path, use_external_data_format=True, all_tensors_to_one_file=True, convert_attribute=True
            )

    print("encoder onnx model saved to", onnx_model_path)

