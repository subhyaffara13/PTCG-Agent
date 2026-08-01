
def validate_onnx_model(
    onnx_model_path,
    example_inputs,
    example_outputs_flatten,
    use_gpu,
    fp16,
    output_names=None,
):
    test_session = create_onnxruntime_session(onnx_model_path, use_gpu, enable_all_optimization=False)
    if test_session is None:
        logger.error(f"{onnx_model_path} is an invalid ONNX model")
        return False

    logger.info(f"{onnx_model_path} is a valid ONNX model")

    # Compare the inference result with PyTorch or Tensorflow
    example_ort_inputs = {k: t.numpy() for k, t in example_inputs.items()}
    example_ort_outputs = test_session.run(output_names, example_ort_inputs)
    if len(example_outputs_flatten) != len(example_ort_outputs):
        logger.error(
            f"Number of output tensors expected {len(example_outputs_flatten)}, got {len(example_ort_outputs)}"
        )
        return False

    for i in range(len(example_outputs_flatten)):
        abs_diff = numpy.amax(numpy.abs(example_ort_outputs[i] - example_outputs_flatten[i].cpu().numpy()))
        if abs_diff > 1e-4:
            logger.info(f"Max absolute diff={abs_diff} for output tensor {i}")

        rtol = 5e-02 if fp16 else 1e-4
        atol = 1e-01 if fp16 else 1e-4
        if not numpy.allclose(
            example_ort_outputs[i],
            example_outputs_flatten[i].cpu().numpy(),
            rtol=rtol,
            atol=atol,
        ):
            logger.error(f"Output tensor {i} is not close: rtol={rtol}, atol={atol}")
            return False

    logger.info(f"inference result of onnxruntime is validated on {onnx_model_path}")
    return True

