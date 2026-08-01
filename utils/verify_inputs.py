
def verify_inputs(beam_inputs, graph_inputs):
    # Verify that ONNX graph's inputs match beam search op's inputs
    beam_required_inputs = list(filter(lambda beam_input: beam_input, beam_inputs))
    assert len(graph_inputs) == len(beam_required_inputs)
    for graph_input, beam_input in zip(graph_inputs, beam_required_inputs, strict=False):
        # Check if graph_input is in beam_input to handle beam_input names with the "_fp16" suffix
        assert graph_input.name in beam_input

