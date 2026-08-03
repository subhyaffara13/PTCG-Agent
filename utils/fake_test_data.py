import random

def fake_test_data(
    batch_size: int,
    sequence_length: int,
    test_cases: int,
    dictionary_size: int,
    verbose: bool,
    random_seed: int,
    input_ids: TensorProto,
    segment_ids: TensorProto,
    input_mask: TensorProto,
    average_sequence_length: int,
    random_sequence_length: bool,
    mask_type: int,
):
    """Create given number of input data for testing

    Args:
        batch_size (int): batch size
        sequence_length (int): sequence length
        test_cases (int): number of test cases
        dictionary_size (int): vocabulary size of dictionary for input_ids
        verbose (bool): print more information or not
        random_seed (int): random seed
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
    assert input_ids is not None

    np.random.seed(random_seed)
    random.seed(random_seed)

    all_inputs = []
    for _test_case in range(test_cases):
        input_1 = fake_input_ids_data(input_ids, batch_size, sequence_length, dictionary_size)
        inputs = {input_ids.name: input_1}

        if segment_ids:
            inputs[segment_ids.name] = fake_segment_ids_data(segment_ids, batch_size, sequence_length)

        if input_mask:
            inputs[input_mask.name] = fake_input_mask_data(
                input_mask, batch_size, sequence_length, average_sequence_length, random_sequence_length, mask_type
            )

        if verbose and len(all_inputs) == 0:
            print("Example inputs", inputs)
        all_inputs.append(inputs)
    return all_inputs


def fake_test_data(
    batch_size,
    sequence_length,
    test_cases,
    dictionary_size,
    verbose,
    random_seed,
    input_ids,
    input_mask,
    global_mask,
    num_global_tokens,
    average_sequence_length,
    random_sequence_length,
):
    """
    Generate fake input data for test.
    """
    assert input_ids is not None

    np.random.seed(random_seed)
    random.seed(random_seed)

    all_inputs = []
    for _ in range(test_cases):
        input_1 = fake_input_ids_data(input_ids, batch_size, sequence_length, dictionary_size)
        inputs = {input_ids.name: input_1}

        if input_mask:
            inputs[input_mask.name] = fake_input_mask_data(
                input_mask, batch_size, sequence_length, average_sequence_length, random_sequence_length
            )

        if global_mask:
            inputs[global_mask.name] = fake_global_mask_data(
                global_mask, batch_size, sequence_length, num_global_tokens
            )

        if verbose and len(all_inputs) == 0:
            print("Example inputs", inputs)
        all_inputs.append(inputs)

    return all_inputs

