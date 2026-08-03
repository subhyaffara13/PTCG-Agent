from typing import Any, Callable

def print_performance(
    model: Callable[..., Any],
    example_inputs: Sequence[Any] = (),
    times: int = 10,
    repeat: int = 10,
    baseline: float = 1.0,
    device: str = "cuda",
) -> float:
    timings = torch.tensor(
        [timed(model, example_inputs, times, device) for _ in range(repeat)]
    )
    took = torch.median(timings) / times
    print(f"{took / baseline:.6f}")
    return took.item()

