
def generate_test_data(
    batch_size: int,
    sequence_length: int,
    test_cases: int,
    seed: int,
    verbose: bool,
    input_ids: TensorProto,
    segment_ids: TensorProto,
    input_mask: TensorProto,
    average_sequence_length: int,
    random_sequence_length: bool,
    mask_type: int,
    dictionary_size: int = 10000,
):
    """Create given number of input data for testing

    Args:
        batch_size (int): batch size
        sequence_length (int): sequence length
        test_cases (int): number of test cases
        seed (int): random seed
        verbose (bool): print more information or not
        input_ids (TensorProto): graph input of input IDs
        segment_ids (TensorProto): graph input of token type IDs
        input_mask (TensorProto): graph input of attention mask
        average_sequence_length (int): average sequence length excluding paddings
        random_sequence_length (bool): whether use uniform random number for sequence length
        mask_type (int): mask type 1 is mask index; 2 is 2D mask; 3 is key len, cumulated lengths of query and key

    Returns:
        List[Dict[str,numpy.ndarray]]: list of test cases, where each test case is a dictionary
                                       with input name as key and a tensor as value
    """
    all_inputs = fake_test_data(
        batch_size,
        sequence_length,
        test_cases,
        dictionary_size,
        verbose,
        seed,
        input_ids,
        segment_ids,
        input_mask,
        average_sequence_length,
        random_sequence_length,
        mask_type,
    )
    if len(all_inputs) != test_cases:
        print("Failed to create test data for test.")
    return all_inputs


def generate_test_data(
    batch_size,
    sequence_length,
    test_cases,
    seed,
    verbose,
    input_ids,
    input_mask,
    global_mask,
    num_global_tokens,
    average_sequence_length,
    random_sequence_length,
):
    dictionary_size = 10000
    all_inputs = fake_test_data(
        batch_size,
        sequence_length,
        test_cases,
        dictionary_size,
        verbose,
        seed,
        input_ids,
        input_mask,
        global_mask,
        num_global_tokens,
        average_sequence_length,
        random_sequence_length,
    )
    if len(all_inputs) != test_cases:
        print("Failed to create test data for test.")
    return all_inputs

