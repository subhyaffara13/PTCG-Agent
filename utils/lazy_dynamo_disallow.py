from typing import Callable

def lazy_dynamo_disallow(func: Callable[_P, _R]) -> Callable[_P, _R]:
    import torch._dynamo

    return torch._dynamo.disallow_in_graph(func)

