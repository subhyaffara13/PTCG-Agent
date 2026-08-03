import itertools
from typing import Any

def check_is_cuda(gm: torch.fx.GraphModule, example_inputs: Iterable[Any]) -> bool:
    return all(x.is_cuda for x in itertools.chain(example_inputs, gm.parameters(True)))

