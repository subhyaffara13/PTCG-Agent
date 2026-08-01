
def _num_outputs(batched_outputs: Tensor | tuple[Tensor, ...]) -> int:
    if isinstance(batched_outputs, tuple):
        return len(batched_outputs)
    return 1


def _num_outputs(batched_outputs: Tensor | tuple[Tensor, ...]) -> int:
    if isinstance(batched_outputs, tuple):
        return len(batched_outputs)
    return 1

