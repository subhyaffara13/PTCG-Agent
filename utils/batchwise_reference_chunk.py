import math


def batchwise_reference_chunk(op, sample):
    # reference for chunk() over dim=0
    B = sample.input.size(0)
    num_chunks = sample.kwargs["chunks"]
    chunk_size = math.ceil(B / num_chunks)
    num_full_chunks = B // chunk_size
    chunk_sizes = [chunk_size for _ in range(num_full_chunks)]
    if B % chunk_size != 0:
        # final chunk contains the leftovers
        chunk_sizes.append(B % chunk_size)

    # split unbound components into chunks according to calculated sizes
    components = list(sample.input.unbind())
    start = 0
    chunks = []
    for chunk_size in chunk_sizes:
        chunks.append(components[start : start + chunk_size])
        start += chunk_size

    # rejoin into NJT outputs
    return [torch.nested.as_nested_tensor(lst, layout=torch.jagged) for lst in chunks]

