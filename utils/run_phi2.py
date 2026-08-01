
def run_phi2(
    onnx_model_path,
    use_buffer_share,
    device_id,
    packed_kv=False,
    use_fp16=True,
    use_step=False,
    use_cuda_graph=False,
    run_benchmark=False,
):
    generator = ORTGenerator(onnx_model_path)
    generator.create_session(device_id, use_fp16, use_buffer_share, packed_kv, use_step, use_cuda_graph)

    def simple_run(prompt):
        example_batch_size = len(prompt)
        if use_cuda_graph:
            generator.append_static_inputs(batch_size=example_batch_size)
        texts = generator.generate(prompt, max_length=210, cuda_graph_annotation=example_batch_size)

        for i in range(len(texts)):
            print("Prompt: ", prompt[i])
            print("Texts: ", texts[i])

    prompt = [
        '''```python
    def print_prime(n):
    """
    Print all primes between 1 and n
    """'''
    ]

    if not run_benchmark:
        simple_run(prompt)

    # Run simple benchmark. Time the decoder only.
    if run_benchmark:
        token_num = 32
        for batch_size in [1, 2, 4, 8]:
            generator.append_static_inputs(batch_size)
            for sequence_length in [16, 512]:
                prompt_shape = (batch_size, sequence_length)
                generator.generate_benchmark(prompt_shape, token_num, cuda_graph_annotation=batch_size)

