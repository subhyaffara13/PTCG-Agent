
def create_longformer_test_data(
    model,
    output_dir,
    batch_size,
    sequence_length,
    test_cases,
    seed,
    verbose,
    input_ids_name,
    input_mask_name,
    global_mask_name,
    num_global_tokens,
    average_sequence_length,
    random_sequence_length,
):
    input_ids, input_mask, global_mask = get_longformer_inputs(model, input_ids_name, input_mask_name, global_mask_name)
    all_inputs = generate_test_data(
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
    )

    for i, inputs in enumerate(all_inputs):
        output_test_data(output_dir, i, inputs)

