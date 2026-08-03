import os

def create_and_save_test_data(
    model: str,
    output_dir: str,
    batch_size: int,
    sequence_length: int,
    test_cases: int,
    seed: int,
    verbose: bool,
    input_ids_name: str | None,
    segment_ids_name: str | None,
    input_mask_name: str | None,
    only_input_tensors: bool,
    average_sequence_length: int,
    random_sequence_length: bool,
    mask_type: int,
):
    """Create test data for a model, and save test data to a directory.

    Args:
        model (str): path of ONNX bert model
        output_dir (str): output directory
        batch_size (int): batch size
        sequence_length (int): sequence length
        test_cases (int): number of test cases
        seed (int): random seed
        verbose (bool): whether print more information
        input_ids_name (str): graph input name of input_ids
        segment_ids_name (str): graph input name of segment_ids
        input_mask_name (str): graph input name of input_mask
        only_input_tensors (bool): only save input tensors,
        average_sequence_length (int): average sequence length excluding paddings
        random_sequence_length (bool): whether use uniform random number for sequence length
        mask_type(int): mask type
    """
    input_ids, segment_ids, input_mask = get_bert_inputs(model, input_ids_name, segment_ids_name, input_mask_name)

    all_inputs = generate_test_data(
        batch_size,
        sequence_length,
        test_cases,
        seed,
        verbose,
        input_ids,
        segment_ids,
        input_mask,
        average_sequence_length,
        random_sequence_length,
        mask_type,
    )

    for i, inputs in enumerate(all_inputs):
        directory = os.path.join(output_dir, "test_data_set_" + str(i))
        output_test_data(directory, inputs)

    if only_input_tensors:
        return

    import onnxruntime  # noqa: PLC0415

    providers = (
        ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if "CUDAExecutionProvider" in onnxruntime.get_available_providers()
        else ["CPUExecutionProvider"]
    )
    session = onnxruntime.InferenceSession(model, providers=providers)
    output_names = [output.name for output in session.get_outputs()]

    for i, inputs in enumerate(all_inputs):
        directory = os.path.join(output_dir, "test_data_set_" + str(i))
        result = session.run(output_names, inputs)
        for i, output_name in enumerate(output_names):  # noqa: PLW2901
            tensor_result = numpy_helper.from_array(np.asarray(result[i]), output_name)
            with open(os.path.join(directory, f"output_{i}.pb"), "wb") as file:
                file.write(tensor_result.SerializeToString())

