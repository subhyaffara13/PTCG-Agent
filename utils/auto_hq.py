from typing import Dict, List, Optional

def auto_hq(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
) -> PathType:
    """Finds the contraction path by automatically choosing the method based on
    how many input arguments there are, but targeting a more generous
    amount of search time than ``'auto'``.
    """
    from opt_einsum.path_random import random_greedy_128

    return _AUTO_HQ_CHOICES.get(len(inputs), random_greedy_128)(inputs, output, size_dict, memory_limit)

