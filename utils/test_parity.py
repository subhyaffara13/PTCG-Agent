
def test_parity(device, model, ort_session, batch_size, sequence_length, global_length, verbose=True):
    parameters = f"batch_size={batch_size} sequence_length={sequence_length} global_length={global_length}"
    logger.info(f"Comparing Torch and ORT outputs for {parameters}...")
    dummy_inputs: LongformerInputs = LongformerHelper.get_dummy_inputs(
        batch_size, sequence_length, global_length, device
    )
    ort_inputs = dummy_inputs.get_ort_inputs()
    ort_outputs = ort_session.run(None, ort_inputs)
    input_list = dummy_inputs.to_list()
    torch_outputs = model(*input_list)
    max_diff = np.amax(torch_outputs[0].cpu().numpy() - ort_outputs[0])
    logger.info(f"last_state max diff = {max_diff}")
    if verbose and (math.isnan(max_diff) or max_diff > 0.001):
        print("torch last_state:", torch_outputs[0])
        print("ort last_state:", ort_outputs[0])
    return float(max_diff)

