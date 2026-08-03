from typing import Any, Callable

def _run_op_on_sample(op: Callable[..., Any], sample: SampleInput) -> Any:
    """Run an operator on a SampleInput, handling both tensor and tuple inputs."""
    if isinstance(sample.input, torch.Tensor):
        return op(sample.input, *sample.args, **sample.kwargs)
    return op(*sample.input, *sample.args, **sample.kwargs)

