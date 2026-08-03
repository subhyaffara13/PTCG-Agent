import functools
from typing import Any, Tuple

def simple_tree_tuple(seq: Sequence[Tuple[int, ...]]) -> Tuple[Any, ...]:
    """Make a simple left to right binary tree out of iterable `seq`.

    ```python
    tuple_nest([1, 2, 3, 4])
    #> (((1, 2), 3), 4)
    ```

    """
    return functools.reduce(lambda x, y: (x, y), seq)

