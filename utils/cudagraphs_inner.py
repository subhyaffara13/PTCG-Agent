from typing import Any, Callable

def cudagraphs_inner(
    model: Callable[..., Any],
    inputs: Sequence[Any],
    copy_outputs: bool = True,
    copy_inputs: bool = True,
) -> Callable[..., Sequence[Any]]:
    """This isn't registered as a backend, but is used in some benchmarks"""
    assert isinstance(inputs, (list, tuple))
    if copy_inputs:
        static_inputs = [torch.zeros_like(x) for x in inputs]
    else:
        static_inputs = list(inputs)

    # warmup
    torch.cuda.synchronize()
    stream = torch.cuda.Stream()
    stream.wait_stream(torch.cuda.current_stream())
    with torch.cuda.stream(stream):
        model(*inputs)
    stream.synchronize()
    torch.cuda.current_stream().wait_stream(stream)
    torch.cuda.synchronize()

    # record
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph, stream=stream):
        static_outputs = model(*static_inputs)
    if not isinstance(static_outputs, (list, tuple)):
        static_outputs = (static_outputs,)

    def run(*new_inputs: Any) -> Sequence[Any]:
        assert len(static_inputs) == len(new_inputs)
        if copy_inputs:
            for dst, src in zip(static_inputs, new_inputs):
                dst.copy_(src)
        graph.replay()
        if copy_outputs:
            return [x.clone() for x in static_outputs]
        else:
            return static_outputs

    return run

