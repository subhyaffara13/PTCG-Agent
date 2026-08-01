
def allocateOutputBuffers(output_buffers, output_buffer_max_sizes, device):  # noqa: N802
    # Allocate output tensors with the largest test size needed. So the allocated memory can be reused
    # for each test run.

    for i in output_buffer_max_sizes:
        output_buffers.append(torch.empty(i, dtype=torch.float32, device=device))

