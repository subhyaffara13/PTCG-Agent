
def load_test_case(dir: str) -> tuple[bytes, Any, Any]:
    """Load a self contained ONNX test case from a directory.

    The test case must contain the model and the inputs/outputs data. The directory structure
    should be as follows:

    dir
    \u251c\u2500\u2500 test_<name>
    \u2502   \u251c\u2500\u2500 model.onnx
    \u2502   \u2514\u2500\u2500 test_data_set_0
    \u2502       \u251c\u2500\u2500 input_0.pb
    \u2502       \u251c\u2500\u2500 input_1.pb
    \u2502       \u251c\u2500\u2500 output_0.pb
    \u2502       \u2514\u2500\u2500 output_1.pb

    Args:
        dir: The directory containing the test case.

    Returns:
        model_bytes: The ONNX model in bytes.
        inputs: the inputs data, mapping from input name to numpy.ndarray.
        outputs: the outputs data, mapping from output name to numpy.ndarray.
    """
    try:
        import onnx
        from onnx import numpy_helper  # type: ignore[attr-defined]
    except ImportError as exc:
        raise ImportError(
            "Load test case from ONNX format failed: Please install ONNX."
        ) from exc

    with open(os.path.join(dir, "model.onnx"), "rb") as f:
        model_bytes = f.read()

    test_data_dir = os.path.join(dir, "test_data_set_0")

    inputs = {}
    input_files = glob.glob(os.path.join(test_data_dir, "input_*.pb"))
    for input_file in input_files:
        tensor = onnx.load_tensor(input_file)  # type: ignore[attr-defined]
        inputs[tensor.name] = numpy_helper.to_array(tensor)
    outputs = {}
    output_files = glob.glob(os.path.join(test_data_dir, "output_*.pb"))
    for output_file in output_files:
        tensor = onnx.load_tensor(output_file)  # type: ignore[attr-defined]
        outputs[tensor.name] = numpy_helper.to_array(tensor)

    return model_bytes, inputs, outputs

